/* http://stackoverflow.com/questions/4495626 */

function VideoContextMenu(e)
{
	$(".custom-menu").finish().toggle(30)
	$(".custom-menu").css({top: (e.pageY - 15) + "px", left: (e.pageX - 2) + "px"});

	return false;
}
$("#mainVideo").bind("contextmenu", VideoContextMenu);

$(document).bind("mousedown", function(e){
	// If the clicked element is not the menu, hide it
	if (!$(e.target).parents(".custom-menu").length > 0)
		$(".custom-menu").hide(20);
});

function ViewAtSource()
{
	var video = $("#mainVideo").get(0);
	if(!video.paused)
		video.pause();

	var path = videoFilename.replace(".mp4", "")
	path = path.replace("youtube ", "http://www.youtube.com/watch?v=");
	path = path.replace("nico ", "http://www.nicovideo.jp/watch/");
	window.open(path);
}
function CopyID()
{
	window.prompt("", videoFilename.replace(".mp4", ""));
}
function ContextMenuAction(e)
{
	if(e.which == 1)
	{
		switch($(this).attr("data-action"))
		{
		case "next":
			location.reload();
			break;
		case "back":
			console.log("Not yet implemented"); // TODO
			break;
		case "source":
			ViewAtSource();
			break;		
		case "copyid":
			setTimeout(CopyID, 20);
			break;
		}
	}

	$(".custom-menu").hide(20);
}
$(".custom-menu li").click(ContextMenuAction);

$(".custom-menu li").bind("contextmenu", function(){return false;});

$("#controlDiv").bind("contextmenu", function(e){return false;});