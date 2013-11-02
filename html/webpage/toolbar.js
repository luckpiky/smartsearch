
function my(formname){
  var url = "http://www.baidu.com/baidu";
  formname.ct.value = "2097152";
  formname.action = url;
  return true;
}


document.write('<div align="center" class="toolbar">');
document.write('<form name="f1" onsubmit="return my(this)" target="_blank">');
document.write('<input name=word size="30" maxlength="100">');
document.write('<input type="submit" value="Search"><br>');
document.write('<input name=tn type=hidden value="bds">');
document.write('<input name=cl type=hidden value="3">');
document.write('<input name=ct type=hidden>');
document.write('<input name=si type=hidden value="www.verycheck.net">');
document.write('</form>');
document.write('</div>');

