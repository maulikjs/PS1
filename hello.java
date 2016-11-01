int count=2
String str= "SELECT * FROM TAGS WHERE "
for( i=0; i<count; i++)
{
  str+="tag.text="+a[i]+"AND"
}
