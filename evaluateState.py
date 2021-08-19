def evaluateState(states):
  #探索木の葉（一番下のノード）の状態を見て評価する関数

  #for文でstates(探索木)の要素をNodeに格納し，一つずつ見ていく
    for Node in states:
      positionPointE=0#AIの駒の位置の点数
      positionPointC=0#Userの駒の位置の点数

      isNearbyE=0 #AIから見てUserの駒が近くにあるか
      isNearbyC=0 #Userから見てAIの駒が近くにあるか


      #葉を探すために子供の数（childNum）を見ていく
      #childNumが0だったらそれは葉である
      #値が入っていない(Noneのとき)も考慮して条件式を書いた
      if Node.childNum==0 or Node.childNum==None:

        #######駒の位置について考える###########
        #AIの駒の座標(E_position)を評価する
        for position in Node.state.E_position:
            positionEmP=position%100#AIの駒の位置を代入(高さなし)

            #座標0から4までなら1点
            #以下同
            if 0<=positionEmP and positionEmP<=4:
                positionPointE=positionPointE+0

            elif 5<=positionEmP and positionEmP<=9:
                positionPointE=positionPointE+1

            elif 10<=positionEmP and positionEmP<=14:
                positionPointE=positionPointE+3

            elif 15<=positionEmP and positionEmP<=19:
                positionPointE=positionPointE+6

            elif 20<=positionEmP and positionEmP<=24:
                positionPointE=positionPointE+10

            elif 25<=positionEmP and positionEmP<=29:
                positionPointE=positionPointE+15

            elif 30<=positionEmP and positionEmP<=34:
                positionPointE=positionPointE+100

            #マスの端っこは点数が低い
            if (positionEmP==0 or
                positionEmP==4 or
                positionEmP==5 or
                positionEmP==9 or
                positionEmP==10 or
                positionEmP==14 or
                positionEmP==15 or
                positionEmP==19 or
                positionEmP==20 or
                positionEmP==24 or
                positionEmP==25 or
                positionEmP==29 ):
                positionPointE=positionPointE-2

        #Userの駒の座標(C_position)を評価する
        for position in Node.state.P_position:
            positionCmP=position%100#Userの駒の位置を代入(高さなし)


            if 0<=positionCmP and positionCmP<=4:
                positionPointC=positionPointC+15

            elif 5<=positionCmP and positionCmP<=9:
                positionPointC=positionPointC+10

            elif 10<=positionCmP and positionCmP<=14:
                positionPointC=positionPointC+6

            elif 15<=positionCmP and positionCmP<=19:
                positionPointC=positionPointC+3

            elif 20<=positionCmP and positionCmP<=24:
                positionPointC=positionPointC+1

            elif 25<=positionCmP and positionCmP<=29:
                positionPointC=positionPointC+0

            #マスの端っこは点数が低い
            if (positionCmP==0 or
                positionCmP==4 or
                positionCmP==5 or
                positionCmP==9 or
                positionCmP==10 or
                positionCmP==14 or
                positionCmP==15 or
                positionCmP==19 or
                positionCmP==20 or
                positionCmP==24 or
                positionCmP==25 or
                positionCmP==29):
                positionPointC=positionPointC-2






        ########相手の駒の周りについて考える##########
        #AIの駒から見てUserの駒が近くにあるか確認
        for positionE in Node.state.E_position:
            positionEm=positionE%100#AIの駒の位置を代入（高さなし）
            for positionC in Node.state.P_position:
                #print("AI:",positionE)
                #print("User",positionC)
                #positionEm=positionE%100#AIの駒の位置を代入（高さなし）
                positionCm=positionC%100#Userの駒の位置を代入（高さなし）

                #近くにUserの駒があるか確認
                #あったら減点する
                #探索木が1個目か3個目の時
                if Node.depth%2==1:
                    if (positionEm==positionCm-6 or
                    positionEm==positionCm-5 or
                    positionEm==positionCm-4 or
                    positionEm==positionCm-1 or
                    positionEm==positionCm+1 or
                    positionEm==positionCm+4 or
                    positionEm==positionCm+5 or
                    positionEm==positionCm+6 ):
                        isNearbyE=isNearbyE-10


                #探索木が2個目か4個目の時
                if Node.depth%2==0:
                    #近くにUserの駒があるか確認
                    #あったら加点する
                    if (positionEm==positionCm-6 or
                    positionEm==positionCm-5 or
                    positionEm==positionCm-4 or
                    positionEm==positionCm-1 or
                    positionEm==positionCm+1 or
                    positionEm==positionCm+4 or
                    positionEm==positionCm+5 or
                    positionEm==positionCm+6 ):
                        isNearbyE=isNearbyE+10


                #Userの駒に乗ってたら加点する
                if positionE+100==positionC:
                    isNearbyE=isNearbyE+15

                #仲間と同じとこに行くと点数が低くなる
                for positionEE in Node.state.E_position:
                    if positionE+100==positionEE:
                        isNearbyE=isNearbyE-4


            #print(isNearbyE)

        #Userの駒から見てAIの駒が近くにあるか確認
        for positionC in Node.state.P_position:
            positionCm=positionC%100#Userの駒の位置を代入（高さなし）
            for positionE in Node.state.E_position:

                positionEm=positionE%100#AIの駒の位置を代入（高さなし）
                #positionCm=positionC%100#Userの駒の位置を代入（高さなし）

                #探索木が1個目か3個目か5個目のとき
                if Node.depth%2==1:
                    #近くにAIの駒があるか確認
                    #あったら加点する
                    if (positionCm==positionEm-6 or
                    positionCm==positionEm-5 or
                    positionCm==positionEm-4 or
                    positionCm==positionEm-1 or
                    positionCm==positionEm+1 or
                    positionCm==positionEm+4 or
                    positionCm==positionEm+5 or
                    positionCm==positionEm+6 ):
                        isNearbyC=isNearbyC-10

                #探索木が2個目か4個目のとき
                if Node.depth%2==0 :
                    #近くにAIの駒があるか確認
                    #あったら減点する
                    if (positionCm==positionEm-6 or
                    positionCm==positionEm-5 or
                    positionCm==positionEm-4 or
                    positionCm==positionEm-1 or
                    positionCm==positionEm+1 or
                    positionCm==positionEm+4 or
                    positionCm==positionEm+5 or
                    positionCm==positionEm+6 ):
                        isNearbyC=isNearbyC+10

                #AIの駒に乗ってたら加点する
                if positionC+100==positionE:
                    isNearbyC=isNearbyC+15


        #今までの得点を合計してeval(評価点)に代入
        if Node.depth%2==1 :
            Node.eval=positionPointE+isNearbyE-(positionPointC+isNearbyC)

        if Node.depth%2==0:
            Node.eval=-(positionPointE+isNearbyE)+(positionPointC+isNearbyC)

    return states
