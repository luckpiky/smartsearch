var agent = navigator.userAgent;
if(agent.indexOf("Android") > -1)
{
	//document.getElementsByTagName("link")[0].href="simple_phone.css";
}
else if(agent.indexOf("iPhone") > -1 || agent.indexOf("iPad") > -1)
{
	//document.getElementsByTagName("link")[0].href="simple_iphone.css";
}
else
{
	//document.getElementsByTagName("link")[0].href="simple_pc.css";
}
