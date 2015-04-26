from nicovideo import Nicovideo
import pafy

def Tests():
	nico = Nicovideo()
	nico.append('sm24245546')
	for v in nico:
		assert v.title == '【第13回MMD杯本選】Paranoia!!!! 【東方MMD-PV】'

	vid = pafy.new("AuJhxd8on-M")
	assert vid.title == '綾倉盟 - Unknown'

	vid = pafy.new("AuJhYd8on-M")

Tests()