sql_name_map = {
	'solar' : {
		#################################
		# Weather measurements with SMA #
		#################################
		#'ExlSolIrr'	: ('Radiation (external)', 'W/m^2'), # always reads 0
		'IntSolIrr'	: ('Radiation', 'W/m^2'),
		'SMA-h-On'	: ('Total Hours On', ''),
		#'TmpAmb' : ('Ambient Temperature', ''), # seems broken.. -273 celcius consistently
		'TmpMdul'	: ('Outside Temperature', ''), #'TmpMdul C', 'TmpMdul F', 'TmpMdul K' <-- unit is encoded in name
		'WindVel'	: ('Wind Speed', ''),#'WindVel m/s' <-- unit is encoded in name
		####################
		# Solar panel info #
		####################
		'A.Ms.Amp'	: ('Unit A DC Current', 'A'),
		'A.Ms.Vol'	: ('Unit A DC Voltage', 'V'),
		'A.Ms.Watt'	: ('Unit A Watts', 'W'),
		'A1.Ms.Amp'	: ('Unit A1 DC Current', 'A'),
		'B.Ms.Amp'	: ('Unit B DC Current', 'A'),
		'B.Ms.Vol'	: ('Unit B DC Voltage', 'V'),
		'B.Ms.Watt'	: ('Unit B Watts', 'W'),
		'B1.Ms.Amp'	: ('Unit B1 DC Current', 'A'),
		'Error'	: ('Error', ''),
		'E-Total'	: ('Total Generated Energy', 'Wh'),
		'GM.TotS0Out'	: ('S0 Grid Feed-in Counter', ''),
		'GM.TotWhOut'	: ('Grid Feed-in Counter Reading', 'Wh'),
		'GridMs.A.phsA'	: ('Grid current phase L1', 'A'),
		'GridMs.A.phsB'	: ('Grid current phase L2', 'A'),
		'GridMs.A.phsC'	: ('Grid current phase L3', 'A'),
		'GridMs.Hz'	: ('Grid Frequency', 'Hz'),
		'GridMs.PhV.phsA'	: ('Grid voltage phase L1', 'V'),
		'GridMs.PhV.phsB'	: ('Grid voltage phase L2', 'V'),
		'GridMs.PhV.phsC'	: ('Grid voltage phase L3', 'V'),
		'GridMs.TotPF'	: ('Displacement power factor', ''),
		'GridMs.TotVA'	: ('Apparent power', 'VA'),
		'GridMs.TotVAr'	: ('Reactive power', 'VAr'),
		'GridMs.VA.phsA'	: ('Apparent power L1', 'VA'),
		'GridMs.VA.phsB'	: ('Apparent power L2', 'VA'),
		'GridMs.VA.phsC'	: ('Apparent power L3', 'VA'),
		'GridMs.VAr.phsA'	: ('Reactive power L1', 'VAr'),
		'GridMs.VAr.phsB'	: ('Reactive power L2', 'VAr'),
		'GridMs.VAr.phsC'	: ('Reactive power L3', 'VAr'),
		'GridMs.W.phsA'	: ('Power L1', 'W'),
		'GridMs.W.phsB'	: ('Power L2', 'W'),
		'GridMs.W.phsC'	: ('Power L3', 'W'),
		#'Inv.TmpLimStt'	: ('Derating', ''),
		'InvCtl.Stt'	: ('Status, device control', ''),
		'Iso.FltA'	: ('Residual current', ''),
		'Mode'	: ('Operating Mode', ''),
		'Mt.TotOpTmh'	: ('Feed-in time', 's'),
		'Mt.TotTmh'	: ('Operating time', 's'),
		#'Op.BckOpStt'	: ('', ''), # ???
		#'Op.EvtCntIstl'	: ('Number of events for installer', ''),
		#'Op.EvtCntUsr'	: ('Number of events for user', ''),
		#'Op.EvtNo'	: ('Current event number', ''),
		#'Op.EvtNoDvlp'	: ('', ''), # ???
		#'Op.GriSwCnt'	: ('Number of grid connections', ''),
		#'Op.GriSwStt'	: ('Grid relay/contactor', ''),
		'Op.Health'	: ('Condition', ''),
		#'Op.Prio'	: ('Recommended action', ''),
		#'Op.TmsRmg'	: ('Waiting time until feed-in', 's'),
		'Pac'	: ('Power', 'W'),
		'PCM-DigInStt'	: ('Status of digital inputs of power control module', ''),
		'PlntCtl.Stt'	: ('Status, PV system control', '')
	},

	'hvac' : {
		
	},

	'weather' : {

	}
}