// lex.js 
var AWS = require('aws-sdk'),
   fs = require('fs'),
   ts = require('tailstream'),
   exec = require('child_process').exec;

   var FULFILLED = 'Fulfilled',
   RESPONSE_FILE = 'response.mpeg',
   REMOVE_REQUEST_FILE = 'rm request.wav',
   RECORD_COMMAND = 'arecord --device=hw:1,0 --format S16_LE --rate 44100 -d 3 -c1 recording.wav',
   streaming = false,
   inputStream,
   lexruntime = new AWS.LexRuntime({
     region: 'us-east-1',
     credentials: new AWS.Credentials(
       'AKIAJJOUN2ESGFUQNI5A',
       'fGeo9g/qD2BGrnjXyhzuoS60DK6GtAnnEcWD7aHo', null)
   });   

var setupStream = function() {
   streaming = true;
   inputStream = ts.createReadStream('./request.wav');
   var params = {
     botAlias: '$LATEST',
     botName: 'Reginald',
     userId: 'lexHeadTesting',
     contentType: 'audio/l16; rate=16000; channels=1',
     inputStream: inputStream
   };

   lexruntime.postContent(params, function(err, data) {
     if (err) {
       console.log(err, err.stack);
       process.exit(1);
     } else {
       fs.writeFile(RESPONSE_FILE, data.audioStream, function(err) {
         if (err) {
           return console.log(err);
           process.exit(1);
         }
       });
       var playback = exec('sudo mpg321 ' + RESPONSE_FILE);
       playback.on('close', function(code) {
         exec('rm ' + RESPONSE_FILE);
         if (data.dialogState !== FULFILLED) {
           streaming = false;
           record();
         }
       });
     }
   });
 }

var record = function() {
   console.log('Listening...')
   var recording = exec(RECORD_COMMAND);
   recording.stderr.on('data', function(data) {
     console.log(data);
     if (!streaming) {
       setupStream();
     }
   });
   recording.on('close', function(code) {
     inputStream.done();
     exec(REMOVE_REQUEST_FILE);
   });
 }
record();