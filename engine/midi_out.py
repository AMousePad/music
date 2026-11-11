"""What every performer hands on: the key strokes for the sampler, a standard MIDI file,
and the pedal curve in the form the sampler wants.

A performer class inherits from PerformanceOutput and, once it has played, provides
    self.events    one dict per key stroke with on, off (seconds), pitch, vel
    self.sustain   (times, values 0..1)   the damper pedal, continuous
    self.soft      (times, values 0..1)   the una corda
    self.sc.title  the title, for the MIDI track name
"""
import numpy as np


class PerformanceOutput:
    def as_notes(self):
        return [(e["on"], e["off"], e["pitch"], e["vel"]) for e in self.events]

    def write_midi(self, path):
        import mido
        tpb = 960
        mid = mido.MidiFile(ticks_per_beat=tpb)
        tr = mido.MidiTrack(); mid.tracks.append(tr)
        tempo = 500000                                  # 120 bpm: 1 tick = 0.52 ms
        tick = lambda sec: int(round(sec * tpb * 1e6 / tempo))
        msgs = []
        for e in self.events:
            msgs.append((tick(e["on"]), 1, mido.Message("note_on", note=e["pitch"], velocity=e["vel"])))
            msgs.append((tick(e["off"]), 0, mido.Message("note_off", note=e["pitch"], velocity=64)))
        for cc, curve in ((64, self.sustain), (67, self.soft)):
            # write ramps as dense steps so any player reproduces half-pedalling
            tt, vv = np.array(curve[0]), np.array(curve[1])
            fine = np.arange(0, tt[-1] + 0.01, 0.01)
            val = np.round(np.interp(fine, tt, vv) * 127).astype(int)
            last = None
            for x, v in zip(fine, val):
                if v != last:
                    msgs.append((tick(x), 0, mido.Message("control_change", control=cc, value=int(v))))
                    last = v
        msgs.sort(key=lambda m: (m[0], m[1]))
        tr.append(mido.MetaMessage("track_name", name=self.sc.title, time=0))
        tr.append(mido.MetaMessage("set_tempo", tempo=tempo, time=0))
        tr.append(mido.Message("program_change", program=0, time=0))
        prev = 0
        for tk, _, m in msgs:
            m.time = tk - prev; prev = tk
            tr.append(m)
        mid.save(path)

    def sustain_for_render(self):
        """dense step curve for the piano engine"""
        tt, vv = np.array(self.sustain[0]), np.array(self.sustain[1])
        fine = np.arange(0, tt[-1] + 0.01, 0.004)
        return (list(fine), list(np.interp(fine, tt, vv)))
