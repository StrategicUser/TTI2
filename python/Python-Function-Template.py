#  --------------------------------
#  Network Device Trunk Filter Function
#  --------------------------------
def setIntf():
	#cdp_list = []
	trunk_list = []
	with open('files/cdp_final.txt', 'w') as cdp_final:
		cnt = 0
		#cnt1 = 0
		for line in cdp_final:
			line = line.strip()
			trunk_list[cnt] = line
			with open('files/ether_final.txt', 'r') as ether_final:
				for line1 in ether_final:
					line1 = line1.strip()
					ether_list = line1.split()
					if line in line1:
						cnt = cnt + 1
						trunk_list[cnt] = ether_list[0]
			cnt = cnt + 1
	print trunk_list

	return(trunk_list)
#  ------------
#  End Function
#  ------------