// (c) Copyright 2017 Sean Connelly (@voidqk) http://sean.cm
// MIT License
// Project Home: https://github.com/voidqk/midimap

var noteroot = 60;  // C is the root
var notes = [
	[ 0, 4, 7],     // I
	[-1, 2, 5, 7],  // V7
	[ 2, 5, 9],     // ii
	[ 1, 4, 9],     // VI
	[-1, 4, 7],     // iii
	[ 0, 5, 9],     // IV
	[ 0, 4, 7, 10], // I7
	[-1, 4, 7],     // V
	[ 2, 6, 9],     // II
	[ 0, 5, 9],     // vi
	[-1, 4, 8],     // III
	[ 0, 5, 8]      // iv
];
var print = ['I', 'V7', 'ii', 'VI', 'iii', 'IV', 'I7', 'V', 'II', 'vi', 'III', 'iv'];
var bass = [0, 7, 2, 9, 4, 5, 0, 7, 2, 9, 4, 5];
var names = ['NoteC', 'NoteDb', 'NoteD', 'NoteEb', 'NoteE', 'NoteF', 'NoteGb', 'NoteG', 'NoteAb',
	'NoteA', 'NoteBb', 'NoteB'];
function nameof(note){
	var oct = Math.floor(note / 12) - 2;
	return names[note % 12] + (oct < 0 ? 'N' + Math.abs(oct) : oct);
}
console.log('# (c) Copyright 2017 Sean Connelly (@voidqk) http://sean.cm');
console.log('# MIT License');
console.log('# Project Home: https://github.com/voidqk/midimap');
for (var oct = 2; oct <= 4; oct++){
	for (var n = 0; n < 12; n++){
		for (var p = 0; p < 2; p++){
			console.log('');
			console.log('OnNote Any ' + names[n] + oct + ' ' + (p == 0 ? '0' : 'Positive'));
			if (p > 0)
				console.log('\tPrint "' + print[n] + '"');
			console.log('\tSendNote Channel ' +
				nameof(noteroot + bass[n] - 12) + ' Value  # Bass Note');
			for (var i = 0; i < notes[n].length; i++)
				console.log('\tSendNote Channel ' + nameof(noteroot + notes[n][i]) + ' Value');
			console.log('End');
		}
		notes[n].push(notes[n].shift() + 12);
	}
}

console.log('');
console.log('OnElse');
console.log('\tSendCopy');
console.log('End');
