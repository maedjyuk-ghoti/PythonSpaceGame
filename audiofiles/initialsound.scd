// Maintenance
s.boot
NetAddr.localAddr

// Bind addresses to synths
(
OSCdef(\explosionlistener, {
	Synth('explosion',[\pitch:50.rrand(600)])
}, "/spacegame/explosion");
)

(
OSCdef(\shotsfiredlistener, {
	Synth('explosion',[\pitch:700])
}, "/spacegame/shotsfired");
)

// Synths
(
SynthDef('explosion', {
	arg pitch = 200;
	var sound = SinOsc.ar(pitch, mul:0.2);
	var linen = Env.linen();
	var env = EnvGen.kr(linen, doneAction:2);
	Out.ar([0,1], sound * env);
}).add;
)

(
SynthDef('\shotsfired', {
	arg pitch = 200;
	var sound = SinOsc.ar(pitch, mul:0.2);
	var linen = Env.linen();
	var env = EnvGen.kr(linen, doneAction:2);
	Out.ar([0,1], sound * env);
}).add;
)


// Maintenance
s.quit