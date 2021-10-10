# -*- coding: utf-8 -*-
import logging

import eastmoneypy
from apscheduler.schedulers.background import BackgroundScheduler

import time
from examples.factors.fundamental_selector import FundamentalSelector
from examples.reports import get_subscriber_emails, stocks_with_info

from zvt.contract.api import get_entities
from zvt.domain import Stock,StockTradeDay,FinanceFactor,BalanceSheet
from zvt.factors.target_selector import TargetSelector
from zvt.factors import BullFactor, CrossMaVolumeFactor
from zvt.factors import MaStatsFactor
logger = logging.getLogger(__name__)

sched = BackgroundScheduler()


# 基本面选股 每周一次即可 基本无变化
#@sched.scheduled_job('cron', hour=0, minute=0, day_of_week='0')
def report_core_company():
    while True:
        error_count = 0
        # email_action = EmailInformer()

        try:
            #datetime.datetime.now()#
            #target_date = to_time_str(now_pd_timestamp())
            target_date = '2021-10-08'
            start = '2018-10-01'
            my_selector: TargetSelector = FundamentalSelector(start_timestamp=start, end_timestamp=target_date)
            # add the factors

            my_selector.run()

            tlong_targets = my_selector.get_open_long_targets(timestamp=target_date)

            my_selector1 = MaStatsFactor(entity_ids=tlong_targets,
                                                              start_timestamp=start, end_timestamp=target_date)

            #my_selector.add_filter_factor(factor2)
            long_targets = my_selector1.get_open_long_targets(timestamp=target_date)

            if long_targets:
                stocks = get_entities(provider='joinquant', entity_schema=Stock, entity_ids=long_targets,
                                      return_type='domain')

                # add them to eastmoney
                try:
                    try:
                        eastmoneypy.del_group('core')
                    except:
                        pass
                    eastmoneypy.create_group('core')
                    for stock in stocks:
                        eastmoneypy.add_to_group(stock.code, group_name='core')
                except Exception as e:
                    logger.exception('report_core_company error:{}'.format(e))
                    # email_action.send_message(zvt_config['email_username'], f'report_core_company error',
                    #                           'report_core_company error:{}'.format(e))

                infos = stocks_with_info(stocks)
                msg = '\n'.join(infos)
                write=''
                for stock in stocks:
                    write = write+ '\'' + f'{stock.code}'+'\','
                write ='[' + write[:-1] + ']'
                f = open("corecompany.txt", 'w')
                f.write(write)
                print('写入文件成功')
                f.close()
            else:
                msg = 'no targets'

            logger.info(msg)

            # email_action.send_message(get_subscriber_emails(), f'{to_time_str(target_date)} 核心资产选股结果', msg)
            break
        except Exception as e:
            logger.exception('report_core_company error:{}'.format(e))
            time.sleep(60 * 3)
            # error_count = error_count + 1
            # if error_count == 10:
            #     email_action.send_message(zvt_config['email_username'], f'report_core_company error',
            #                               'report_core_company error:{}'.format(e))


if __name__ == '__main__':
    #init_log('report_core_company.log')

    report_core_company()

    #sched.start()

    #sched._thread.join()
