with open("rawtext.txt","r") as f:
    text = f.read().replace("\n"," ").split(". ")



for i in text:
    print(i)
    l = input("(Positive,Negative,Empty)>")
    with open("data.txt","a") as f:
        f.write(f"{i}------{l}\n")