row = '004BasicTypeOverall-10'

begin = int(row[:int(row.find('-'))])

print(begin)

end = int(row[(int(row.find('-')))+1:])

print(end)

#length= end - begin
length = int(row[(int(row.find('-')))+1:]) - int(row[:int(row.find('-'))])

print(length)