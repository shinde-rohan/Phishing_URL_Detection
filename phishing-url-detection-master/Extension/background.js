chrome.extension.onRequest.addListener(function(prediction){
    if (prediction == 1){
        alert("Warning: This website might be a phishing website !!!");
    }
    else if (prediction == -1){
        //alert("No phishing detected");
    }
});
