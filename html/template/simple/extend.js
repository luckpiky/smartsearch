<script language="javascript">
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
</script>

