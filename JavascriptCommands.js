window.location.href = 'https://www.fandango.com/site-index/movietheaters.html';
var arr = [], l = document.links;
for(var i=0; i<l.length; i++) {
  arr.push(l[i].href);
}

window.location.href='/a-wrinkle-in-time-203789/movie-overview';

var test = window.open('theaters/ak.html');
a = test.document.links;
var test2= window.open(a[1])
b=test2.document.links;
test3=window.open('https://tickets.fandango.com/Transaction/Ticketing/ticketboxoffice.aspx?row_count=215194132&tid=aajnh&sdate=2018-03-05+22:20&mid=204224&from=mov_det_showtimes');
test3.document.getElementById("AreaRepeater_TicketRepeater_0_quantitytb_0").value= "1"

C:\Program Files (x86)\Google\Chrome\Application>chrome.exe -incognito -disable-web-security --user-data-dir