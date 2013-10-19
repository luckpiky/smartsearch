var agent = navigator.userAgent;
if(agent.indexOf("Android") > -1 || agent.indexOf("ios") > -1)
{
	document.getElementsByTagName("link")[0].href="simple_phone.css";
}
else
{
	document.getElementsByTagName("link")[0].href="simple_pc.css";
}
