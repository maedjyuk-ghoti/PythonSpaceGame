// this example is basically like OSCFunc.trace but filters out
// /status.reply messages
(
f = { |msg, time, addr|
    if(msg[0] != '/status.reply') {
        "time: % sender: %\nmessage: %\n".postf(time, addr, msg);
    }
};
thisProcess.addOSCRecvFunc(f);
);
NetAddr.localAddr
// stop posting.
thisProcess.removeOSCRecvFunc(f);

//simple page 2 sounds
// pushes
(
OSCdef(\push1listener, { |msg|
	if (msg[1] == 1) {
		Synth(\shotsfired, [\pitch:1000])
	}
}, "/2/push1");

OSCdef(\push2listener, { |msg|
	if (msg[1] == 1) {
		Synth(\explosion)
	}
}, "/2/push2");

OSCdef(\push3listener, { |msg|
	if (msg[1] == 1) {
		Synth(\explode)
	}
}, "/2/push3");

OSCdef(\push4listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push4");

OSCdef(\push5listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push5");

OSCdef(\push6listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push6");

OSCdef(\push7listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push7");

OSCdef(\push8listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push8");

OSCdef(\push9listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push9");

OSCdef(\push10listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push10");

OSCdef(\push11listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push11");

OSCdef(\push12listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push12");

OSCdef(\push13listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push13");

OSCdef(\push14listener, {
	Synth()
}, "/2/push14");

OSCdef(\push15listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push15");

OSCdef(\push16listener, { |msg|
	if (msg[1] == 1) {
		Synth()
	}
}, "/2/push16");

// toggles
OSCdef(\toggle1listener, {
	Synth()
}, "/2/toggle1");

OSCdef(\toggle2listener, {
	Synth()
}, "/2/toggle2");

OSCdef(\toggle3listener, {
	Synth()
}, "/2/toggle3");

OSCdef(\toggle4listener, {
	Synth()
}, "/2/toggle4");

// player shoot
SynthDef(\shotsfired, {
	arg pitch = 1000;
	var sound = SinOsc.ar(XLine.kr(pitch, pitch - 800, 0.1, doneAction:2), mul:0.2);
	var linen = Env.linen();
	var env = EnvGen.kr(linen, doneAction:2);
	Out.ar([0,1], sound * env);
}).add;

// object explosion
SynthDef(\explosion, {
	arg pitch = 200;
	var sound = SinOsc.ar(pitch, mul:0.2);
	var linen = Env.perc();
	var env = EnvGen.kr(linen, doneAction:2);
	Out.ar([0,1], sound * env);
}).add;

// player crash
c = Pbind(
	\amp, 0.5,
	\scale, Scale.major,
	\degree, Pseq([8, 6, 4, 5, 3, 1], 1),
	\dur, Pseq([
		Pseq([0.125],
			5), 0.5], inf),
	\octave, 5,
);

// test explosion
SynthDef(\explode, {
	arg i_out, freq = 200, gate = 1, pan=0.5, amp=0.1;
	var ae,sig;

	ae = EnvGen.kr(Env.asr(0, 1, 0.05, 1, 0), doneAction:2);
	sig = Impulse.ar(0);
	sig = LPF.ar(FreeVerb2.ar(sig, sig, 1, 0.1, 0.4), freq);
	sig = (sig * 5000).tanh;
	sig = LPF.ar(sig, 8000);

	Out.ar([0, 1], amp*ae*sig);
}).add;

)