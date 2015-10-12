// Maintenance
s.boot;
NetAddr.localAddr;

// Bind addresses to synths
(
OSCdef(\explosionlistener, {
	Synth(\explosion,[\pitch:200])
}, "/spacegame/explosion");
)

(
OSCdef(\shotsfiredlistener, {
	Synth(\shotsfired,[\pitch:1000])
}, "/spacegame/shotsfired");
)

// Synths
// TODO Better explosion sound.
(
SynthDef(\explosion, {
	arg pitch = 200;
	var sound = SinOsc.ar(pitch, mul:0.2);
	var linen = Env.perc();
	var env = EnvGen.kr(linen, doneAction:2);
	Out.ar([0,1], sound * env);
}).add;
)

(
SynthDef(\shotsfired, {
	arg pitch = 200;
	var sound = SinOsc.ar(XLine.kr(pitch, pitch - 800, 0.1, doneAction:2), mul:0.2);
	var linen = Env.linen();
	var env = EnvGen.kr(linen, doneAction:2);
	Out.ar([0,1], sound * env);
}).add;
)


// Maintenance
s.quit


// test space, not officially implemented yet. Subject to deletion
(
OSCdef(\gamestartlistener, {
	o.play
}, "/spacegame/gamestart");
)

(
SynthDef(\sin, {
	arg freq = 440,
	    dur = 1,
	    amp = 0.5,
	    pan = 0;
	var sine,
		env,
		panner;
    sine = SinOsc.ar(freq, 0, amp);
    env = EnvGen.kr(Env.perc(0.01, dur), doneAction:2);
    panner = Pan2.ar(sine, pan, env);
	Out.ar([0, 1], panner);
}).add
)

(
o = Pbind(
	\instrument, \sin,
	\amp, 0.5,
	\scale, Scale.major,
	\degree, Pseq([0, 2, 4, 1, 3, 5, 4, 6, 8], 1),
	\dur, Pseq([0.125], inf),
	\octave, 5,
);
)

(
OSCdef(\crashlistener, {
	c.play
}, "/spacegame/crash");
)
(
c = Pbind(
	\amp, 0.5,
	\scale, Scale.major,
	\degree, Pseq([8, 6, 4, 5, 3, 1], 1),
	\dur, Pseq([
		Pseq([0.125],
			5), 0.5], inf),
	\octave, 5,
);
)
