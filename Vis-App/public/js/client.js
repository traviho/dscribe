'use strict'

//connection to socket
const socket = io.connect();

//================= CONFIG =================
// Stream Audio
let bufferSize = 2048,
	AudioContext,
	context,
	processor,
	input,
	globalStream;

//vars
let audioElement = document.querySelector('audio'),
	finalWord = false,
	resultText = document.getElementById('ResultText'),
	wordCountChartElement = document.getElementById('wordCountChart'),
	removeLastSentence = true,
	streamStreaming = false,
	recognitionDataArray = [],
	interimSentence = '',
	finalSentence = '',
	internCurrentHoCount = 0,
	internTotalHoCount = 0,
	publicTotalHoCount = 0;

let params = {
	startedRecording: false,
}

var wordCountMap = {};
var wordCountChart;
const chartOptions = {
	scales: {
		yAxes: [{
			ticks: {
				beginAtZero:true
			}
		}]
	}
}
const datasetOptions = {
	label: 'Word Count',
	backgroundColor: [
		'rgba(255, 99, 132, 0.2)',
		'rgba(54, 162, 235, 0.2)',
		'rgba(255, 206, 86, 0.2)',
		'rgba(75, 192, 192, 0.2)',
		'rgba(153, 102, 255, 0.2)',
		'rgba(255, 159, 64, 0.2)'
	],
	borderColor: [
		'rgba(255,99,132,1)',
		'rgba(54, 162, 235, 1)',
		'rgba(255, 206, 86, 1)',
		'rgba(75, 192, 192, 1)',
		'rgba(153, 102, 255, 1)',
		'rgba(255, 159, 64, 1)'
	],
	borderWidth: 1
}


//audioStream constraints
const constraints = {
	audio: true,
	video: false
};

//================= RECORDING =================



function initRecording() {
	socket.emit('startGoogleCloudStream', ''); //init socket Google Speech Connection
	streamStreaming = true;
	AudioContext = window.AudioContext || window.webkitAudioContext;
	context = new AudioContext();
	processor = context.createScriptProcessor(bufferSize, 1, 1);
	processor.connect(context.destination);
	context.resume();

	var handleSuccess = function (stream) {
		globalStream = stream;
		input = context.createMediaStreamSource(stream);
		input.connect(processor);

		processor.onaudioprocess = function (e) {
			microphoneProcess(e);
		};
	};

	navigator.mediaDevices.getUserMedia(constraints)
		.then(handleSuccess);

}

function microphoneProcess(e) {
	var left = e.inputBuffer.getChannelData(0);
	// var left16 = convertFloat32ToInt16(left); // old 32 to 16 function
	var left16 = downsampleBuffer(left, 44100, 16000)
	socket.emit('binaryData', left16);
}

//================= CHART =================
function addWordsToMap(sentence) {
	var words = sentence.split(/\s+/);
	words.forEach(word => {
		if (wordCountMap[word] == null) 
		{
			wordCountMap[word] = 1;
		} else {
			wordCountMap[word] += 1;
		}
	});
}

function getDataFromWordCountMap(wordCountMap) {
	return {
		labels: Object.keys(wordCountMap),
		datasets: [{
			data: Object.values(wordCountMap),
			...datasetOptions
		}]
	}
}

function updateWordCountChart(sentence) {
	addWordsToMap(sentence)
	if (wordCountChart == null) {
		let ctx = wordCountChartElement.getContext('2d');
		wordCountChart = new Chart(ctx, {
			type: 'bar',
			data: {},
			options: chartOptions
		});
	}
	wordCountChart.data = getDataFromWordCountMap(wordCountMap);
	wordCountChart.update();
}

//================= INTERFACE =================
var startButton = document.getElementById("startRecButton");
startButton.addEventListener("click", startRecording);

var endButton = document.getElementById("stopRecButton");
endButton.addEventListener("click", stopRecording);
endButton.disabled = true;

function startRecording() {
	if (params.startedRecording){return}
	params.startedRecording = true;
	endButton.disabled = false;
	initRecording();
}

function stopRecording() {
	endButton.disabled = true;

	if (!streamStreaming){return} // stop disconnecting if already disconnected;

	streamStreaming = false;
	socket.emit('endGoogleCloudStream', '');


	let track = globalStream.getTracks()[0];
	track.stop();

	input.disconnect(processor);
	processor.disconnect(context.destination);
	context.close().then(function () {
		input = null;
		processor = null;
		context = null;
		AudioContext = null;
		startButton.disabled = false;
	});
}

//================= SOCKET IO =================
socket.on('connect', function (data) {
	socket.emit('join', 'Server Connected to Client');
});


socket.on('messages', function (data) {
	console.log(data);
});


socket.on('speechData', function (data) {
	var dataFinal = undefined || data.results[0].isFinal;

	if (dataFinal === false) {
		// processing for interim results
	} else if (dataFinal === true) {
		let finalString = data.results[0].alternatives[0].transcript;
		updateWordCountChart(finalString);

		finalWord = true;
		endButton.disabled = false;
		removeLastSentence = false;
	}
});

//================= OTHER STUFF =================

window.onbeforeunload = function () {
	if (streamStreaming) { socket.emit('endGoogleCloudStream', ''); }
};

//================= SANTAS HELPERS =================

// sampleRateHertz 16000 //saved sound is awefull
function convertFloat32ToInt16(buffer) {
	let l = buffer.length;
	let buf = new Int16Array(l / 3);

	while (l--) {
		if (l % 3 == 0) {
			buf[l / 3] = buffer[l] * 0xFFFF;
		}
	}
	return buf.buffer
}

var downsampleBuffer = function (buffer, sampleRate, outSampleRate) {
    if (outSampleRate == sampleRate) {
        return buffer;
    }
    if (outSampleRate > sampleRate) {
        throw "downsampling rate show be smaller than original sample rate";
    }
    var sampleRateRatio = sampleRate / outSampleRate;
    var newLength = Math.round(buffer.length / sampleRateRatio);
    var result = new Int16Array(newLength);
    var offsetResult = 0;
    var offsetBuffer = 0;
    while (offsetResult < result.length) {
        var nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio);
        var accum = 0, count = 0;
        for (var i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
            accum += buffer[i];
            count++;
        }

        result[offsetResult] = Math.min(1, accum / count)*0x7FFF;
        offsetResult++;
        offsetBuffer = nextOffsetBuffer;
    }
    return result.buffer;
}

function capitalize(s) {
	if (s.length < 1) {
		return s;
	}
	return s.charAt(0).toUpperCase() + s.slice(1);
}