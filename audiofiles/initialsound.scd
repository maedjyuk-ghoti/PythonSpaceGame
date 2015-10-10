s.boot

NetAddr.localAddr

(
SynthDef('explosion', {
	arg pitch = 200;
	var sound = SinOsc.ar(pitch, mul:0.2);
	var linen = Env.linen();
	var env = EnvGen.kr(linen, doneAction:2);
	Out.ar(0, sound * env);
}).add;
)

(
OSCdef(\explosionlistener, {
	Synth('explosion',[\pitch:110])
}, "/spacegame/explosion");
)

s.quit