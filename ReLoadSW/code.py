"""
74シリーズ(14ピン)の確認プログラム(CircuitPython)
"""

import board, digitalio, busio, alarm, time
from ST7032i import ST7032i


### 初期設定 ############################################################
# 入出力     0 3.3V     1 GND      2 3.3V     3 GND 
myPinFix = ( board.GP0, board.GP1, board.GP6, board.GP15 )
myPinsFix = []
for ii, pin in enumerate( myPinFix ) :		# enumerate(添字)込みの繰り返し
	tmp_pin = digitalio.DigitalInOut( pin )	# 端子の指定
	tmp_pin.direction = digitalio.Direction.OUTPUT	# 出力
	myPinsFix.append( tmp_pin )						# リスト追加
	if ii % 2 == 0 : myPinsFix[ii].value = True		# 3.3V
	else           : myPinsFix[ii].value = False	# GND


# LCD（i2C）の設定
i2c = busio.I2C( board.GP27, board.GP26 )	# 端子指定
while not i2c.try_lock() : pass				# これないと動かない！
i2c.scan()									# アドレス
lcd = ST7032i( i2c )						# LCDに渡す
lcd.set_entry_mode( False, False )			# 　動作モード
lcd.set_contrast( 3 )						# 　明るさ
lcd.clear()									#	とりあえず初期化



# 入力パターン
myINPUT  = ( ( 0, 0 ),
	    	 ( 0, 1 ),
			 ( 1, 0 ),
			 ( 1, 1 ) )
# 出力パターン
myOUTPUT = ( ( 1, 1, 1, 0 ),
			 ( 1, 0, 0, 0 ),
			 ( 1, 0 ),
			 ( 0, 0, 0, 1 ),
		 	 ( 0, 1, 1, 1 ),
		 	 ( 0, 1, 1, 0 ) )


# 74シリーズ(14ピン) 1:In	0:Out
#          Num   Name    1   2   3   4   5   6   8   9  10  11  12  13
IC = ( 	( "00", "NAND",  1,  1,  0,  1,  1,  0,  0,  1,  1,  0,  1,  1 ),
    	( "02", "NOR",   0,  1,  1,  0,  1,  1,  1,  1,  0,  1,  1,  0 ),
	 	( "04", "NOT",   1,  0,  1,  0,  1,  0,  0,  1,  0,  1,  0,  1 ),
	 	( "08", "AND",   1,  1,  0,  1,  1,  0,  0,  1,  1,  0,  1,  1 ),
	 	( "32", "OR",    1,  1,  0,  1,  1,  0,  0,  1,  1,  0,  1,  1 ),
	 	( "86", "Ex-OR", 1,  1,  0,  1,  1,  0,  0,  1,  1,  0,  1,  1 )
	)

# 各ICの真理値表一致数 [IC数][0:真理値表適合数  1:稼働状態]
NumMatch = [ [ 0, "" ] for ii in range( len( IC ) ) ]
#         3 IC-1      4 IC-2      5 IC-3      6 IC-4     7 IC-5      8 IC-6
myPin = ( board.GP3,  board.GP4,  board.GP5,  board.GP2, board.GP13, board.GP14,
#         9 IC-8      10 IC-9     11 IC-10    12 IC-11   13 IC-12    14 IC-13
		  board.GP12, board.GP11, board.GP10, board.GP9, board.GP8,  board.GP7 )
myPins = []
for ii in myPin :
	tmp = digitalio.DigitalInOut( ii )
	tmp.direction.OUTPUT	# とりあえず出力モードで格納
	myPins.append( tmp )	# リストに追加



def myJudge() :
	for ii, ic in enumerate( IC ) :	# ロジックIC種で繰り返し
		for jj, io in enumerate( ic ) : 
			if   jj==0 : myID = io		# ロジックICのID（etc：NAND=00）
			elif jj==1 : myName = io	# 　　〃　　の名前
			elif jj>=2 :
				# 入出力の再設定
				if   io==0 : myPins[jj-2].switch_to_input( digitalio.Pull.UP )		# 入力（プルアップ）
				elif io==1 : myPins[jj-2].direction = digitalio.Direction.OUTPUT	# 出力

		# ICの入出力関係の確認(真理値表との比較)
		#  Case NOT ※I/Oのassignが異なる
		if myName=="NOT" :
			for icNum in range( 0, 11, 2 ) :
				# 真理値表との比較
				NumMatch[ii][0] = 0
				for jj in range( 2 ) :
					if icNum<6 :	# 前半
						myPins[ icNum+0 ].value = myINPUT[jj][1] # 入力
						if myPins[ icNum+1 ].value==myOUTPUT[ii][jj] : NumMatch[ii][0] += 1 # 真理値表との比較
					else : 			# 後半
						myPins[ icNum+1 ].value = myINPUT[jj][1] # 入力
						if myPins[ icNum+0 ].value==myOUTPUT[ii][jj] : NumMatch[ii][0] += 1 # 真理値表との比較

				# 表示用テキストの生成
				if NumMatch[ii][0]==2	: NumMatch[ii][1] += str( icNum//2 + 1 ) 	# ok
				else 					: NumMatch[ii][1] += str( "x" )				# NG
			
			if NumMatch[ii][1].count( "x" ) == 6: NumMatch[ii][0] = -1
			NumMatch[ii][1] += "/6"
			print( myID + "(", myName ,")\t : " + NumMatch[ii][1] )
		

		#  Case NOR ※I/Oのassignが異なる
		elif myName=="NOR" :
			for icNum in range( 0, 11, 3 ) :
				# 真理値表との比較
				NumMatch[ii][0] = 0
				for jj in range( 4 ) :
					if icNum<6 :	# 前半
						myPins[ icNum+2 ].value = myINPUT[jj][0] # 入力
						myPins[ icNum+1 ].value = myINPUT[jj][1] # 入力
						if myPins[ icNum+0 ].value==myOUTPUT[ii][jj] : NumMatch[ii][0] += 1 # 真理値表との比較
					else :			# 後半
						myPins[ icNum+0 ].value = myINPUT[jj][0] # 入力
						myPins[ icNum+1 ].value = myINPUT[jj][1] # 入力
						if myPins[ icNum+2 ].value==myOUTPUT[ii][jj] : NumMatch[ii][0] += 1 # 真理値表との比較
				
				# 表示用テキストの生成
				if NumMatch[ii][0]==4	: NumMatch[ii][1] += str( icNum//3 + 1 ) 	# ok
				else 					: NumMatch[ii][1] += str( "x" )				# NG
			
			if NumMatch[ii][1].count( "x" )==4 : NumMatch[ii][0] = -1
			NumMatch[ii][1] += "__/4"
			print( myID + "(", myName ,")\t : " + NumMatch[ii][1] )


		# Case OtherIC
		else :
			tmpTxt = ""
			for icNum in range( 0, 11, 3 ) :
				# 真理値表との比較
				NumMatch[ii][0] = 0
				for jj in range( 4 ) :
					if icNum<6 :	# 前半
						myPins[ icNum+0 ].value = myINPUT[jj][0] # 入力
						myPins[ icNum+1 ].value = myINPUT[jj][1] # 入力
						if myPins[ icNum+2 ].value==myOUTPUT[ii][jj] : NumMatch[ii][0] += 1 # 真理値表との比較
					else :			# 後半
						myPins[ icNum+2 ].value = myINPUT[jj][0] # 入力
						myPins[ icNum+1 ].value = myINPUT[jj][1] # 入力
						if myPins[ icNum+0 ].value==myOUTPUT[ii][jj] : NumMatch[ii][0] += 1 # 真理値表との比較

				# 表示用テキストの生成
				if NumMatch[ii][0]==4	: NumMatch[ii][1] += str( icNum//3 + 1 ) 	# ok
				else 					: NumMatch[ii][1] += str( "x" )				# NG

			if NumMatch[ii][1].count( "x" )==4 : NumMatch[ii][0] = -1
			NumMatch[ii][1] += "__/4"
			print( myID + "(", myName ,")\t : " + NumMatch[ii][1] )


	# もっとも一致したIC情報を液晶に表示
	print("------------------------------------")
	id = 0
	flag = False
	for ii, ic in enumerate( IC ) :
		if NumMatch[ii][0]!=-1 : 
			if NumMatch[id][0] <= NumMatch[ii][0] : id = ii ; flag = True

	lcd.clear()
	if flag == False :
		print( "UnKnown!" )
		lcd.set_cursor( 0, 0 ); lcd.print( 'UnKnown!' )
		lcd.set_cursor( 0, 1 ); lcd.print( '????????' )
		time.sleep( 0.5 )

	else :
		print( IC[id][0] + "(", IC[id][1] ,")\t : " + NumMatch[id][1] )
		lcd.set_cursor( 0, 0 ); lcd.print( str( IC[id][0] + " " + IC[id][1] ) )
		lcd.set_cursor( 0, 1 ); lcd.print( NumMatch[id][1] )
		time.sleep( 0.5 )

	for ii, ic in enumerate( IC ) : NumMatch[ii][1] = "" # ReSet



lcd.set_cursor( 0, 0 ); lcd.print( 'Set 74xx' )
lcd.set_cursor( 0, 1 ); lcd.print( 'Push SW!' )
while True :
	myAlarm = alarm.pin.PinAlarm( pin=board.GP28, value=False, pull=True )	# Light Sleepのトリガ（スイッチが押される）
	alarm.light_sleep_until_alarms( myAlarm )								# 
	myJudge( ) # 判定処理
