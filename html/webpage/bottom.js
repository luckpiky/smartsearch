document.write("浙ICP备10207150号");

//百度统计
var _bdhmProtocol = (("https:" == document.location.protocol) ? " https://" : " http://");
document.write(unescape("%3Cscript src='" + _bdhmProtocol + "hm.baidu.com/h.js%3Fd0a9249d63662e8ea0e61c573722901b' type='text/javascript'%3E%3C/script%3E"));



function mysize()
{
  var agent = navigator.userAgent
  h = window.innerHeight;
  w = window.screen.width;

  if(agent.indexOf("Android") > -1 || agent.indexOf("ios") > -1  || agent.indexOf("iPad") > -1  || agent.indexOf("iPhone") > -1)
  {

  }
  else
  {
    document.getElementById("glb").style.width = 800 + "px";
  }
}
window.resize = mysize();
window.addEventListener("onorientationchange" in window ? "orientationchange": "resize", mysize, true);


