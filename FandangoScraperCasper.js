//Problem is that then() gets loaded up in an array, so while loops are EXTREMELY tricky since things aren't getting evaluated right away
//need to use array = array.concat(array2);
//Need to use recursion for looping 
//https://stackoverflow.com/questions/14250151/casperjs-clicking-links-in-a-nested-loop
//https://stackoverflow.com/a/11957919


// Set the start URL which is fandangos list of theaters
var startUrl = 'https://www.fandango.com/site-index/movietheaters.html';

// URL variables
var stateLabels = [];
var theaterLinks = [];

function fandangoSpiderNext(match) {
    switch(match) {
        case 'STATES':
            return fandangoSpiderState;
            break;
        case 'THEATERS':
            return fandangoSpiderTheater;
            break;
        case 'MOVIEDATE1':
            return fandangoSpiderMovieDate1;
            break;
        case 'MOVIEDATE2':
            return fandangoSpiderMovieDate2;
    }
}



function fandangoSpiderState(stateLabels) {
    if (stateLabels.length > 0) {
        addLinks.call(this);
        this.run(check);
    } else {
        this.echo("All done.");
        this.exit();
    }
}


// Get the links, and add them to the links array
// (It could be done all in one step, but it is intentionally splitted)
function addLinks() {
    this.then(function() {
        var found = this.evaluate(searchLinks);
        this.echo(found.length + " links found");
        theaterLinks = theaterLinks.concat(found);
    });
}

// Fetch all <a> elements from the page and return
// the ones which contains a href starting with 'http://'
function searchLinks() {
    var filter, map;
    filter = Array.prototype.filter;
    map = Array.prototype.map;
    return map.call(filter.call(document.querySelectorAll("a"), function(a) {
        return (/./).test(a.getAttribute("href"));
    }), function(a) {
        return a.getAttribute("href");
    });
}

//New Date object for today
var today = new Date();

//Now find the 2 days of they week as indices (from 0 to 6) in a length 2 Array that we want to check the movie price for. First day will be tomorrow. 
//The Second day will be on a weekend if the First day was a weekday. 
//The Second day will be a weekday if the First day was on a weekend.
var dayOfWeek = today.getDay();
//Need to add 1 to day of week to get Tomorrow's date, since we won't be searching for movie prices for today's date
dayOfWeek=dayOfWeek+1;
//DIFF serves to give the second date to check movie prices for the second day
var diff = 6-dayOfWeek;
var secondDay;
if (diff <= 0) {
  diff = 2;
}

//This is the array we will be using. The fandango page has the links for the movie dates using the same indices as below
var twodates=[1,1+diff];

//Scope when using casper has some weird behavior, so we have to define the variables here and use while loops
var boolTest=false;
var i = 0;
var j = 0;
var k = 0;
var l = 0;
//Keep track of the number of clicks to keep track of how many times we need to go back
var numClicks=0;


// Create instances
var casper = require('casper').create({
    verbose: true,
    logLevel: 'error'
})

// Spider from the given Fandango State list
function fandangoSpider(url) {

	// Open the URL
	casper.open(url).then(function() {
        casper.log('this is a debug message', 'debug');
		// Set the status style based on server status code
		var status = this.status().currentHTTPStatus;
		switch(status) {
			case 200: var statusStyle = { fg: 'green', bold: true }; break;
			case 404: var statusStyle = { fg: 'red', bold: true }; break;
			 default: var statusStyle = { fg: 'magenta', bold: true }; break;
		}

		// Display the spidered URL and status
		this.echo(this.colorizer.format(status, statusStyle) + ' ' + url);

		// Find labels present on this page, these happen to all be clickable URL's
		stateLabels = this.evaluate(function() {
            var links = document.links;
            var hrefs=[];
            //returning an array of strings that are the HREFS
            for (ll=0; ll < document.links.length; ll++) {
                hrefs.push(document.links[ll].text);
            }
			return hrefs;
        });

        //Now crawl through all the theaters in USA. So, the counter should only go up to 51!
        while (i < 2) {
            //Clicks on an unvisited State link in America. Will work because links that are visited will be selectors of E:visited only
            this.thenClickLabel(stateLabels[i]).then(function() {
                numClicks++;
            }).then(function() {
                theaterLabels = this.evaluate(function() {
                    var links = document.links;
                    var hrefs=[];
                    //returning an array of strings that are the HREFS
                    for (ll=0; ll < document.links.length; ll++) {
                        hrefs.push(document.links[ll].text);
                    }
                    return hrefs;
                });
            }).then(function() {
                while (j < 2) {
                    //Clicks on an unvisited State link in America. Will work because links that are visited will be selectors of E:visited only
                    this.thenClickLabel(theaterLabels[i]).then(function() {
                        numClicks++;
                    });
                }
            })
            }


            casper.open(stateLinks[i]).then(function() {
        		// Find links present on this page. Still need .HREF to access a link
                var tempLinks = this.evaluate(function() {
                    var links = document.links;
                    var hrefs=[];
                    //returning an array of strings that are the HREFS
                    for (ll=0; ll < document.links.length; ll++) {
                        hrefs.push(document.links[ll].href);
                    }
                    return hrefs;
                });
                this.echo(tempLinks.length);
                theaterLinks.concat(tempLinks);
                this.echo(theaterLinks.length);
            });
            i = i + 1;
        }
        this.echo(theaterLinks.length);
        //theaterLinks.forEach(function(e) {
        while (j < 2) {
            casper.open(theaterLinks[j]).then(function() {
                //There is a calender with clickable dates for the following week (but many times less than a week)
                var theaterdates = this.evaluate(function() {
                    var hrefs=[];
                    var temp = document.getElementsByClassName('date-picker__link');
                    try {
                        hrefs.push(temp[1].href);
                    }
                    catch(error) {
                        //There weren't enough dates available on Fandango at this theater
                    }
                    try {
                        hrefs.push(temp[1+diff]);
                    }
                    catch(error) {
                        //Second date is missing, but should still be ok
                    }
                    //returning an array of strings that are the HREFS
                    return hrefs;
                });
                casper.log('The state website ' + stateLinks[i] + ' and the theater site ' + theaterLinks[j] + ' have this many calender wheel dates ' + theaterdates.length, 'debug');
            });
            j = j + 1;
        }
        //});
	});

}

// Start the Fandango Scraper through Casper
casper.start(startUrl, function() {
	fandangoSpider(startUrl);
});

// Start the run
casper.run();