
import random
import copy
field = [[0,0,0,0,0],
         [0,0,0,0,0],
         [0,0,1,0,0],
         [0,0,0,0,0],
         [0,0,0,0,0]]
continues = None
what = "start"#input("\n")
ignoreL = False
ignoreR = False
ignoreU = False
ignoreD = False
paralyzed = False
lightnings = 0
died_reason = None
hurricane = False



if what.title() == "Start":
     stop = False
     frame_field = ""
     for row in field:
         for cell in row:
             frame_field += str(cell)
         frame_field += '\n'
         frame_field = frame_field.replace('0', '⬛').replace('1', '🔴')
     print(frame_field)
     row = 2
     column = 2

while stop == False:
    if ignoreL == True and ignoreU == True and ignoreR == True and ignoreD == True:
        died_reason = "Uh, I can't move!"
        break
    moves = ['u','r','d','l']
    what = input("Direction: ")#random.choice(moves)
    if paralyzed == True:
        allow_move = random.choice([True, False])
        if allow_move == True:
            what = what
        else:
            if ignoreL == True and what.title() == "L" or ignoreU == True and what.title() == "U" or ignoreR == True and what.title() == "R" or ignoreD == True and what.title() == "D":
                continue
            else:
                what = "You can't move!"
    if what.title() == "L":
         if column != 0 and field[row][column - 1] == 4:
             hurr = random.randint(0, 4)
             cane = random.randint(0, 4)
             if field[hurr][cane] == 2 or field[hurr][cane] == 4:
                 died_reason = "Uhhh, is that dot in the sky you?"
                 field[row][column] = 0
             elif field[hurr][cane] == 0:
                 field[hurr][cane] = 1
                 field[row][column] = 0
                 row = int(hurr)
                 column = int(cane)
         elif column != 0 and field[row][column - 1] != 2:
             field[row][column] = 0
             field[row][column - 1] = 1
             row = row
             column = column - 1
             ignoreL = False
         else:
             ignoreL = True
             continue

    elif what.title() == "R":
         if column != 4 and field[row][column + 1] == 4:
             hurr = random.randint(0, 4)
             cane = random.randint(0, 4)
             if field[hurr][cane] == 2 or field[hurr][cane] == 4:
                 died_reason = "Uhhh, is that dot in the sky you?"
                 field[row][column] = 0
             elif field[hurr][cane] == 0:
                 field[hurr][cane] = 1
                 field[row][column] = 0
                 row = int(hurr)
                 column = int(cane)
         elif column != 4 and field[row][column + 1] != 2:
             field[row][column] = 0
             field[row][column + 1] = 1
             row = row
             column = column + 1
             ignoreR = False
         else:
             ignoreR = True
             continue

    elif what.title() == "U":
         if row != 0 and field[row - 1][column] == 4:
             hurr = random.randint(0, 4)
             cane = random.randint(0, 4)
             if field[hurr][cane] == 2 or field[hurr][cane] == 4:
                 died_reason = "Uhhh, is that dot in the sky you?"
                 field[row][column] = 0
             elif field[hurr][cane] == 0:
                 field[hurr][cane] = 1
                 field[row][column] = 0
                 row = int(hurr)
                 column = int(cane)
         elif row != 0 and field[row - 1][column] != 2:
             field[row][column] = 0
             field[row - 1][column] = 1
             row = row - 1
             column = column
             ignoreU = False
         else:
             ignoreU = True
             continue

    elif what.title() == "D":
         if row != 4  and field[row + 1][column] == 4:
             hurr = random.randint(0, 4)
             cane = random.randint(0, 4)
             if field[hurr][cane] == 2 or field[hurr][cane] == 4:
                 died_reason = "Uhhh, is that dot in the sky you?"
                 field[row][column] = 0
             elif field[hurr][cane] == 0:
                 field[hurr][cane] = 1
                 field[row][column] = 0
                 row = int(hurr)
                 column = int(cane)
         elif row != 4  and field[row + 1][column] != 2:
             field[row][column] = 0
             field[row + 1][column] = 1
             row = row + 1
             column = column
             ignoreD = False
         else:
             ignoreD = True
             continue
    elif what == "You can't move!":
        print(what)


    frag = random.randint(0,4)
    ment = random.randint(0,4)
    chance = random.randint(1,100)
    if chance < 8:
        if hurricane == False:
            print("I wonder why it is so cloudy...\nOh no!It is 🌀ԋυɾɾιƈαɳҽ🌀!")
            while True:
                 if field[frag][ment] != 4:
                     if field[frag][ment] == 1:
                         hurr = random.randint(0, 4)
                         cane = random.randint(0, 4)
                         if field[hurr][cane] == 2 or field[hurr][cane] == 4:
                             died_reason = "Uhhh, is that dot in the sky you?"
                         elif field[hurr][cane] == 0:
                             field[hurr][cane] = 1
                             row = int(hurr)
                             column = int(cane)
                         field[frag][ment] = 4
                         hurricane = True
                         break
                     else:
                         field[frag][ment] = 4
                         hurricane = True
                         break
                 else:
                     frag = random.randint(0, 4)
                     ment = random.randint(0, 4)
        elif hurricane == True:
            Hlines = 4
            Hcells = 4
            while True:
                if field[Hlines][Hcells] == 4:
                    field[Hlines][Hcells] = 0
                Hcells = Hcells - 1
                if Hcells < 0:
                    Hcells = 4
                    Hlines = Hlines - 1
                if Hlines < 0:
                    hurricane = False
                    break

    elif chance < 18:
        print("I wonder why it is so cloudy...\nOh no!It is 🌩️𝘵𝘩𝘶𝘯𝘥𝘦𝘳𝘴𝘵𝘰𝘳𝘮🌩️!")
        ligh = random.randint(0, 4)
        ning = random.randint(0, 4)
        strike = False
        strike_field = copy.deepcopy(field)
        lightnings = random.randint(0,4)
        while strike == False:
            if strike_field[ligh][ning] != 3 and strike_field[ligh][ning] != 4:
                if strike_field[ligh][ning] == 1:
                    para_dea_chance = random.randint(1,5)
                    if para_dea_chance == 1:
                        paralyzed = True
                        just_paralyzed = True
                    else:
                        died_reason = "So ʂԋσƙ⚡ɳɠ expiriance!"
                        field[ligh][ning] = 0
                elif strike_field[ligh][ning] == 2:
                    field[ligh][ning] = 0
                strike_field[ligh][ning] = 3
                if lightnings == 0:
                    strike = True
                else:
                    lightnings = lightnings - 1
            else:
                strike = False
                ligh = random.randint(0, 4)
                ning = random.randint(0, 4)
        strike_field_show = ""
        for lineS in strike_field:
            for cellS in lineS:
                strike_field_show += str(cellS)
            strike_field_show += '\n'
        strike_field_show = strike_field_show.replace('0', '⬛').replace('1', '🔴').replace('2', '❌').replace('3', '⚡').replace('4', '🌪️')
        print(strike_field_show)



    elif chance < 101:
        fall = False
        while fall == False:
             if field[frag][ment] != 2 and field[frag][ment] != 4:
                 if field[frag][ment] == 1:
                     died_reason = "Oh...You've got smashed..."
                 field[frag][ment] = 2
                 fall = True
             else:
                 fall = False
                 frag = random.randint(0, 4)
                 ment = random.randint(0, 4)
    frame_field = ""
    for line in field:
         for cell in line:
             frame_field += str(cell)
         frame_field += '\n'
         frame_field = frame_field.replace('0', '⬛').replace('1', '🔴').replace('2', '❌').replace('4', '🌪️')
    print(frame_field)
    if paralyzed == True and just_paralyzed == True:
        print("You've been paralyzed...")
        just_paralyzed = False

    lineAKAfield = field[0] + field[1] + field[2] + field[3] + field[4]
    if died_reason != None:
        print(died_reason)
        break
    if not 0 in lineAKAfield:
        print("ყơų ῳıŋ!")
        quit()
    if 1 in lineAKAfield:
         if column != 0 and field[row][column - 1] != 2:
             ignoreL = False
         else:
             ignoreL = True
         if column != 4 and field[row][column + 1] != 2:
             ignoreR = False
         else:
             ignoreR = True
         if row != 0 and field[row - 1][column] != 2:
             ignoreU = False
         else:
             ignoreU = True
         if row != 4 and field[row + 1][column] != 2:
             ignoreD = False
         else:
             ignoreD = True
         continue
    else:
         break


print("G⃨a⃨m⃨e⃨ O⃨v⃨e⃨r⃨...")
quit()






























