fo = open("./goodcompany.txt", "w+")
list ='000513,000568,000596,000661,000799,000858,000975,002001,002007,002020,002120,002127,002206,002287,002294,002304,002318,002381,002382,002391,002405,002466,002557,002558,002568,002582,002619,002677,002695'
line = fo.write(list[:-1])
print(line)
fo.close()