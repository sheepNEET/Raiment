import nicovideo as nicolib
import pafy

def Tests():
	nico = nicolib.Nicovideo()
	nico.append('sm24245546')
	for v in nico:
		assert v.title == '【第13回MMD杯本選】Paranoia!!!! 【東方MMD-PV】'

	vid = nicolib.Video('sm24245546')
	assert vid.title == '【第13回MMD杯本選】Paranoia!!!! 【東方MMD-PV】'
	assert vid.video_id == 'sm24245546'
	assert vid.user_id == '7458747'

	vid = pafy.new("AuJhxd8on-M")
	assert vid.title == '綾倉盟 - Unknown'

Tests()
print('Success')