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
                      
            positionEmP=position#AIの駒の位置を代入(高さなし)

            #高さの情報をなくして判断（平面で考える）
            if (200<=positionEmP):
              positionEmP=positionEmP-200

            if (100<=positionEmP):
              positionEmP=positionEmP-100

            #座標1から5までなら0点
            #以下同
            if 1<=positionEmP and positionEmP<=5:
             positionPointE=positionPointE+1

            elif 6<=positionEmP and positionEmP<=10:
              positionPointE=positionPointE+2

            elif 11<=positionEmP and positionEmP<=15:
              positionPointE=positionPointE+3
          
            elif 16<=positionEmP and positionEmP<=20:
              positionPointE=positionPointE+4
          
            elif 21<=positionEmP and positionEmP<=25:
              positionPointE=positionPointE+5
          
            elif 26<=positionEmP and positionEmP<=30:
              positionPointE=positionPointE+6

            #マスの端っこは点数が低い
            if (positionEmP==1,6,11,16,21,26,5,10,15,20,25,30):
              positionPointE=positionPointE-1

        #Userの駒の座標(C_position)を評価する
        for position in Node.state.P_position:

          positionCmP=position#Userの駒の位置を代入

          #高さの情報をなくして判断（平面で考える）
          if 200<=positionCmP:
            positionCmP=positionCmP-200

          if 100<=positionCmP:
            positionCmP=positionCmP-100


          if 1<=positionCmP and positionCmP<=5:
               positionPointC=positionPointC+6

          elif 6<=positionCmP and positionCmP<=10:
               positionPointC=positionPointC+5

          elif 11<=positionCmP and positionCmP<=15:
               positionPointC=positionPointC+4
          
          elif 16<=positionCmP and positionCmP<=20:
               positionPointC=positionPointC+3
          
          elif 21<=positionCmP and positionCmP<=25:
               positionPointC=positionPointC+2
          
          elif 26<=positionCmP and positionCmP<=30:
               positionPointC=positionPointC+1
          
          #マスの端っこは点数が低い
          if (positionCmP==1,6,11,16,21,26,5,10,15,20,25,30):
               positionPointC=positionPointC-1



        ########相手の駒の周りについて考える##########
        #AIの駒から見てUserの駒が近くにあるか確認
        for positionE in Node.state.E_position:
          for positionC in Node.state.P_position:
            #print("AI:",positionE)
            #print("User",positionC)
            positionEm=positionE#AIの駒の位置を代入
            positionCm=positionC#Userの駒の位置を代入


            #高さの情報をなくして判断（平面で考える）
            if 200<=positionEm:
              positionEm=positionEm-200

            if 100<=positionEm:
              positionEm=positionEm-100

            if 200<=positionCm:
              positionCm=positionCm-200

            if 100<=positionCm:
              positionCm=positionCm-100

            #探索木が1個目か3個目か5個目のとき  
            if Node.depth%2==1:
              #近くにUserの駒があるか確認
              #あったら-1する
              if (positionEm==positionCm-6 or
                positionEm==positionCm-5 or
                positionEm==positionCm-4 or 
                positionEm==positionCm-1 or 
                positionEm==positionCm+1 or 
                positionEm==positionCm+4 or 
                positionEm==positionCm+5 or 
                positionEm==positionCm+6 ):
                isNearbyE=isNearbyE-1

            #探索木が2個目か4個目の時
            if Node.depth%2==0:
              #近くにUserの駒があるか確認
              #あったら+1する
              if (positionEm==positionCm-6 or
                positionEm==positionCm-5 or
                positionEm==positionCm-4 or 
                positionEm==positionCm-1 or 
                positionEm==positionCm+1 or 
                positionEm==positionCm+4 or 
                positionEm==positionCm+5 or 
                positionEm==positionCm+6 ):
                isNearbyE=isNearbyE+1
              

            #Userの駒に乗ってたら+2する
            if positionEm==positionCm and positionC<positionE:
              isNearbyE=isNearbyE+2

            #print(isNearbyE)

        #Userの駒から見てAIの駒が近くにあるか確認
        for positionC in Node.state.P_position:
          for positionE in Node.state.E_position:

            
            positionEm=positionE#AIの駒の位置を代入
            positionCm=positionC#Userから見てAIの駒が近くにあるか

            #高さの情報をなくす（平面で考える）
            if 200<=positionEm:
              positionEm=positionEm-200

            if 100<=positionEm:
              positionEm=positionEm-100

            if 200<=positionCm:
              positionCm=positionCm-200

            if 100<=positionCm:
              positionCm=positionCm-100

            #探索木が1個目か3個目か5個目のとき
            if Node.depth%2==1:
              #近くにAIの駒があるか確認
              #あったら+1する
              if (positionCm==positionEm-6 or 
                 positionCm==positionEm-5 or 
                 positionCm==positionEm-4 or 
                 positionCm==positionEm-1 or
                 positionCm==positionEm+1 or 
                 positionCm==positionEm+4 or 
                 positionCm==positionEm+5 or 
                 positionCm==positionEm+6 ):
                isNearbyC=isNearbyC+1

            #探索木が2個目か4個目のとき
            if Node.depth%2==1:
              #近くにAIの駒があるか確認
              #あったら-1する
              if (positionCm==positionEm-6 or 
                 positionCm==positionEm-5 or 
                 positionCm==positionEm-4 or 
                 positionCm==positionEm-1 or
                 positionCm==positionEm+1 or 
                 positionCm==positionEm+4 or 
                 positionCm==positionEm+5 or 
                 positionCm==positionEm+6 ):
                isNearbyC=isNearbyC-1

             #AIの駒に乗ってたら+2する
            if positionCm==positionEm and positionE<positionC:
              isNearbyC=isNearbyC+2




        #今までの得点を合計してeval(評価点)に代入
        Node.eval=positionPointE+isNearbyE-(positionPointC+isNearbyC)

    return states