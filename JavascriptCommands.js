window.location.href = 'https://www.fandango.com/site-index/movietheaters.html';
var arr = [], l = document.links;
var today = new Date();
for(var i=0; i<l.length; i++) {
  var states = window.open(l[i].href);
  var m = states.document.links;
  for(var j=0; j<m.length; j++) {
    var listMoviesToday = window.open(m[j].href);
    var dayOfWeek = today.getDay();
    //Need to add 1 to day of week to get Tomorrow's date, since we won't be searching for movie prices for today's date
    dayOfWeek=dayOfWeek+1;
    //DIFF serves to give the second date to check movie prices for the second date. If Tomorrow's Day of week is Weekend, then the second date will be a weekday.
    var diff = 6-dayOfWeek;
    var secondDay;
    if (diff <= 0) {
      diff = 2;
    }
    var theaterdates = listMoviesToday.document.getElementsByClassName('date-picker__link');
    var twoDates = [];
    try {
      twoDates = [theaterdates[1]];
    }
    catch(error) {
      //There weren't enough dates available on Fandango at this theater
    }
    try {
      twoDates.push(theaterdates[1+diff]);
    }
    catch(error) {
      //Second date is missing, but should still be ok
    }
    for (var t=0; t < twoDates.length; t++) {
      var listMovies = window.open(twoDates[t].href);
      var n = listMovies.document.getElementsByClassName('btn showtime-btn showtime-btn--available');
      for (var k=0; k<n.length; k++) {
        var order = window.open(n[k].document.href);
        var o = order.document.getElementsByClassName("qtyDropDown");
        var boolDropDown=true;
        if (o.length == 0) {
          o = order.document.getElementsByClassName("input_txt");
          boolDropDown=false;
        }
        for (var ii=0; ii < o.length; ii++) {

        }
      }
    }
  }
}

function insertOrder(o, quantity, boolDropDown) {
  if (boolDropDown) {
    o.document.getElementById
  }
}

class ticket {
  constructor(price, movieTitle, theaterName, date, url) {
    this.price = price;
    this.movieTitle=movieTitle;
    this.theaterName=theaterName;
    this.date=date;
    this.url=url;
  }
}

window.location.href='/a-wrinkle-in-time-203789/movie-overview';

var test = window.open('theaters/ak.html');
a = test.document.links;
var test2= window.open(a[1])
b=test2.document.links;
test3=window.open('https://tickets.fandango.com/Transaction/Ticketing/ticketboxoffice.aspx?row_count=215194132&tid=aajnh&sdate=2018-03-05+22:20&mid=204224&from=mov_det_showtimes');
test3.document.getElementById("AreaRepeater_TicketRepeater_0_quantitytb_0").value= "1"

//"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -incognito -disable-web-security --user-data-dir
//Still need to handle case where theater is CLOSED




var arr = [], l = document.links;
var today = new Date();
for(var i=0; i<3; i++) {
  var states = window.open(l[i].href);
  //consider changing this from complete to interactive, but need to watch out for when it is complete but not interactive
  while (states.document.readyState !='interactive' && states.document.readyState !='complete') {
    console.log('waiting')
  }
  console.log(states.document.head);
}




l = document.links;
var today = new Date();
for(var i=0; i<1; i++) {
  var states = window.open(l[i].href);
  while (states.document.readyState !='interactive' && states.document.readyState !='complete') {
    console.log('waiting')
  }
  var m = states.document.links;
  for(var j=0; j<m.length; j++) {
    var listMoviesToday = window.open(m[j].href);
    while (listMoviesToday.document.readyState !='interactive' && listMoviesToday.document.readyState !='complete') {
      console.log('waiting')
    }
    var dayOfWeek = today.getDay();
    //Need to add 1 to day of week to get Tomorrow's date, since we won't be searching for movie prices for today's date
    dayOfWeek=dayOfWeek+1;
    //DIFF serves to give the second date to check movie prices for the second date. If Tomorrow's Day of week is Weekend, then the second date will be a weekday.
    var diff = 6-dayOfWeek;
    var secondDay;
    if (diff <= 0) {
      diff = 2;
    }
    var theaterdates = listMoviesToday.document.getElementsByClassName('date-picker__link');
    var twoDates = [];
    try {
      twoDates = [theaterdates[1]];
    }
    catch(error) {
      //There weren't enough dates available on Fandango at this theater
    }
    try {
      twoDates.push(theaterdates[1+diff]);
    }
    catch(error) {
      //Second date is missing, but should still be ok
    }
/*     for (var t=0; t < twoDates.length; t++) {
      var listMovies = window.open(twoDates[t].href);
      var n = listMovies.document.getElementsByClassName('btn showtime-btn showtime-btn--available');
      for (var k=0; k<n.length; k++) {
        var order = window.open(n[k].document.href);
        var o = order.document.getElementsByClassName("qtyDropDown");
        var boolDropDown=true;
        if (o.length == 0) {
          o = order.document.getElementsByClassName("input_txt");
          boolDropDown=false;
        }
        for (var ii=0; ii < o.length; ii++) {

        }
      }
    } */
  }
}


l = document.links;
var today = new Date();
var test;
for(var i=0; i<2; i++) {
  var states = window.open(l[i].href);
  while (states.document.readyState !='interactive' && states.document.readyState !='complete') {
    console.log('waiting')
  }
  var m = states.document.links;
  test = m;
}
