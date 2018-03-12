window.location.href = 'https://www.fandango.com/site-index/movietheaters.html';
stateLinks = document.links;
var today = new Date();
for(var i=0; i<stateLinks.length; i++) {
  console.log("Opening " + stateLinks[i].text);
  statei = window.open(stateLinks[i].href);
  statei.addEventListener("load", openStateTheaters(statei.document.links));
}


function openStateTheaters(theaterLinks, today) {
  for (var j = 0; j < theaterLinks.length; j++) {
    console.log("Opening " + theaterLinks[j].text);
    theateri = window.open(theaterLinks[j]);
    theateri.addEventListener("load", openTheater(theateri, today));
  }
}

function openTheater(theateri, today) {
  todayMovieLinks=theateri.document.links;
  var dayOfWeek = today.getDay();
  //Need to add 1 to day of week to get Tomorrow's date, since we won't be searching for movie prices for today's date
  dayOfWeek=dayOfWeek+1;
  //DIFF serves to give the second date to check movie prices for the second date. If Tomorrow's Day of week is Weekend, then the second date will be a weekday.
  var diff = 6-dayOfWeek;
  var secondDay;
  if (diff <= 0) {
    diff = 2;
  }
  var theaterdates = theateri.document.getElementsByClassName('date-picker__link');
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
  for (var k = 0; k < twoDates.length; k++) {
    dayMoviesPage=window.open(twoDates[k]);
    dayMoviesPage.addEventListener("load", openMoviesOnDay(dayMoviesPage))
    openMoviesOnDay(twoDates[k]);
  }
}

function openMoviesOnDay(dateLink) {
  dayMoviesPage=window.open(dateLink.href);
  dayMoviesPage.addEventListener("load", function(event) {
    dayMoviesList=dayMoviesPage.document.links;
    for (var l = 0; l < dayMoviesList.length; l++) {
      openMovie(dayMoviesList[l]);
    }
  });
  
}

function openMovie()



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

//"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -incognito -disable-web-security --user-data-dir


a=document.links;
b=window.open(a[0]);
b.addEventListener("load", function(event) {
    console.log("All resources finished loading!");
    c=b.document.links;
    d=window.open(c[0]);
  });
