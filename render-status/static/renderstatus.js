function httpGet(URL)
{
    // get html
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", URL, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function notifyComplete(jobname) {
    // notify the user that the job is complete
    var notification = new Notification(jobname + " has finished rendering!");
}

function notifyCheck() {
    // function to check if browser notifications are enabled
    if (Notification.permission !== "denied") {
        Notification.requestPermission().then(function (permission) {
          // If the user accepts, let's create a notification
          if (permission === "granted") {
              console.log("Notifications Enabled");
            // var notification = new Notification("notifications enabled!");
          }
        });
      }
}

function increment()
{
    // function that runs continuously, checking the webapp for render updates, and updating the page.

    // get the json render status from the webapp
    let jsonResult = JSON.parse(httpGet("/status"));

    // first delete any jobs that don't exist anymore in the new json
    let currentCards = document.getElementsByClassName("card");
    let cardIds = [];
    let jsonIds = [];
    for (var job of jsonResult)
    {
        jsonIds.push(job.name);
    }

    for (var card of currentCards)
    {
        if (jsonIds.indexOf(card.id.toString()) == -1)
        {
            card.remove();
            console.log(card.id + ' removed');
        }
    }

    currentCards = document.getElementsByClassName("card");

    for (var card of currentCards)
    {
        if (jsonIds.indexOf(card.id.toString()) >= 0)
        {
            cardIds.push(card.id.toString());
        }
    }

    console.log(cardIds);

    // then make a new card for each new job in the json.

    let cardContainer = document.querySelector("#cardContainter");
    let template = document.getElementsByTagName("template")[0];

    for (var job of jsonResult)
    {
        console.log(job.name + ' ' + cardIds.indexOf(job.name.toString()));
        if(cardIds.indexOf(job.name.toString()) == -1)
        {
            console.log(job.name + ' doesnt exist in document');
            // Clone the new row and insert it into the table
            let clone = template.content.cloneNode(true);
            let mainCard = clone.querySelector("#mainCard");
            mainCard.id = job.name;
            let title = clone.querySelector("#cardTitle");
            title.innerHTML = job.name;
            let prog = clone.querySelector("#prog");
            prog.innerHTML = job.percent + '%';
            prog.style.width = job.percent + '%';
            
            let deleteMe = clone.querySelector("#deleteName");
            deleteMe.value = job.name;

            cardContainer.insertBefore(clone, cardContainer.firstChild);
        }
    }

    // then update all the cards that are now shown

    currentCards = document.getElementsByClassName("card");

    for (var card of currentCards)
    {
        let currentId = card.id;
        let progress = 0;
        for (var job of jsonResult)
        {
            if (currentId == job.name)
            {
                progress = job.percent;
            }
        }

        let prog = card.querySelector("#prog");

        if (prog.innerHTML != "100%" && progress == 100)
        {
            notifyComplete(currentId);
        }

        prog.innerHTML = progress + '%';
        prog.style.width = progress + '%';
        prog.className = "progress-bar progress-bar-striped progress-bar-animated";

        if (progress == 100)
        {
            prog.className = "progress-bar bg-success";
        }
    }

}

// increment once to build the page, then check if browser notifications are enabled, then continuosly update the page.

increment();
notifyCheck()
window.setInterval(increment, 1000);