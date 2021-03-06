var currentVideoWidth = 0;
var currentVideoHeight = 0;
function VideoMetadata()
{
	currentVideoWidth = $("#mainVideo").get(0).videoWidth;
	currentVideoHeight = $("#mainVideo").get(0).videoHeight;
}

function SeekChange()
{
	var video = $("#mainVideo").get(0);
	var newTime = video.duration * ($("#seekBar").val() / 100)
	video.currentTime = newTime;
}
$("#seekBar").change(SeekChange);

function UpdateSeekBar()
{
	var video = $("#mainVideo").get(0);
	$("#seekBar").val(100 * (video.currentTime / video.duration));
}
$("#mainVideo").bind("timeupdate", UpdateSeekBar);

function VolumeChange()
{
	var video = $("#mainVideo").get(0);
	video.volume = $("#volumeBar").val() / 100;
}
$("#volumeBar").change(VolumeChange);

function IsFullscreen()
{
	if(document.webkitIsFullScreen)
		return document.webkitIsFullScreen;
	else if(document.mozFullScreen)
		return document.mozFullScreen;
	else
		return (document.fullScreenElement && document.fullScreenElement !== null);
}

// On window resize (including after fullscreen toggle)
// - resize video
// - resize controls to match video's width
function OnResize()
{
	if(IsFullscreen())
	{
		var vidWidth = $("#mainVideo").get(0).offsetWidth;
		var vidHeight = $("#mainVideo").get(0).offsetHeight;
		var vidRatio = vidWidth/vidHeight;
		var winWidth = $(window).width();
		var winHeight = window.screen.availHeight; //$(window).height() glitches on Firefox
		var winRatio = winWidth/winHeight;
		if(vidRatio > winRatio)
		{
			//vid is longer than window
			$("#mainVideo").css("min-width", $(window).width());
			$("#mainVideo").css("min-height", "");

		}
		else if(vidRatio < winRatio)
		{
			//window is longer than vid
			$("#mainVideo").css("min-width", "");
			$("#mainVideo").css("min-height", window.screen.availHeight);
		}
		else
		{
			//exactly the same ratio
			$("#mainVideo").css("min-width", $(window).width());
			$("#mainVideo").css("min-height", window.screen.availHeight);
		}
		$("#mainVideo").css("max-width", $(window).width());
		$("#mainVideo").css("max-height", window.screen.availHeight);

		if(isFirefox)
		{
			$("#mainVideo").css("position", "relative");
			$("#mainVideo").css("top", "50%");
			$("#mainVideo").css("transform", "translateY(-50%)");
		}	
	}
	else
	{
		var vidWidth = currentVideoWidth ? currentVideoWidth : $("#mainVideo").get(0).offsetWidth;
		var vidHeight = currentVideoHeight ? currentVideoHeight : $("#mainVideo").get(0).offsetHeight;
		var vidRatio = vidWidth/vidHeight;
		var areaWidth = $(window).width() - 120;
		var areaHeight = $(window).height() - 60 - 40;
		var areaRatio = areaWidth/areaHeight;

		function ClampWidth(x)
		{
			if(x < 640)
				return 640;
			if(x > areaWidth)
				return areaWidth;
			return x;
		}

		if(vidRatio > areaRatio)
		{
			//vid is longer than area?
			if(vidWidth > areaWidth)
				var predictWidth = areaWidth;
			else
				var predictWidth = ClampWidth(vidWidth);
		}
		else if(vidRatio < areaRatio)
		{
			var predictWidth = ClampWidth(vidWidth);
		}
		else
		{
			var predictWidth = ClampWidth(vidWidth);
		}
		$("#controlDiv").width(predictWidth);

		$("#mainVideo").css("min-width", "640px");
		$("#mainVideo").css("max-width", areaWidth);
		$("#mainVideo").css("min-height", "480px");
		$("#mainVideo").css("max-height", areaHeight);

		if(isFirefox)
		{
			$("#mainVideo").css("position", "");
			$("#mainVideo").css("top", "");
			$("#mainVideo").css("transform", "");
		}
	}
}
$(window).resize(OnResize);
$("#mainVideo").resize(OnResize);
$("#videoDiv").resize(OnResize);

// On left click
// - play/pause
// On double left click
// - toggle fullscreen
function TogglePlay()
{
	var video = $("#mainVideo").get(0);
	if(video.paused)
		video.play();
	else
		video.pause();
}
function ToggleFullscreen()
{
	var video = $("#videoDiv").get(0);
	if(!IsFullscreen())
	{
		if (video.requestFullscreen)
			video.requestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
		else if (video.msRequestFullscreen)
			video.msRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
		else if (video.mozRequestFullScreen)
			video.mozRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
		else if (video.webkitRequestFullscreen)
			video.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
	}
	else
	{
		if (document.cancelFullScreen)
			document.cancelFullScreen();
		else if (document.exitFullScreen)
			document.exitFullScreen();
		else if (document.mozCancelFullScreen)
			document.mozCancelFullScreen();
		else if (document.webkitCancelFullScreen)
			document.webkitCancelFullScreen();
		else if (document.webkitExitFullScreen)
			document.webkitExitFullScreen();
		else if(document.msExitFullscreen)
			document.msExitFullscreen();
	}
}
var timeSinceClick = 0;
var lastMouseTimeout;
function OnVideoClick(e)
{
	if(e.which == 1) //left click
	{
		if(($.now() - timeSinceClick) < 350)
		{
			clearTimeout(lastMouseTimeout);
			ToggleFullscreen();
		}
		else
		{
			timeSinceClick = $.now();
			lastMouseTimeout = setTimeout(TogglePlay, 350);
		}
	}
}
$("#mainVideo").mousedown(OnVideoClick);

// On space bar
// - play/pause
function KeyboardHandler(e)
{
	if(e.which == 32) //space
		TogglePlay();
}
$(window).keyup(KeyboardHandler);