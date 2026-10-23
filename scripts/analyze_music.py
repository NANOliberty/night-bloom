import sys, numpy as np, librosa, json

def analyze(path):
    y, sr = librosa.load(path, sr=22050, mono=True)
    dur = len(y)/sr
    hop = sr  # 1-second windows
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
    rms_db = 20*np.log10(rms+1e-9)
    rms_db -= rms_db.max()
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    # percussive energy per second (drum presence)
    y_h, y_p = librosa.effects.hpss(y)
    perc = librosa.feature.rms(y=y_p, frame_length=2048, hop_length=hop)[0]
    perc_db = 20*np.log10(perc+1e-9); perc_db -= perc_db.max()
    # spectral centroid per second (brightness)
    cent = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop)[0]
    # vocal-ish energy: harmonic energy in 200-4000 Hz band with high flatness? crude: harmonic rms in 300-3000 band
    S = np.abs(librosa.stft(y_h, n_fft=2048, hop_length=hop))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    band = (freqs>=300)&(freqs<=3000)
    vocal_band = S[band].sum(axis=0); total = S.sum(axis=0)+1e-9
    vocal_ratio = vocal_band/total
    n = min(len(rms_db), len(perc_db), len(cent), len(vocal_ratio))
    out = {"dur": round(dur,1), "tempo": round(float(np.atleast_1d(tempo)[0]),1)}
    # summarize per 15s block
    blocks=[]
    for s in range(0, n, 15):
        e = min(s+15, n)
        blocks.append({"t": f"{s//60}:{s%60:02d}", "loud": round(float(rms_db[s:e].mean()),1),
                       "drums": round(float(perc_db[s:e].mean()),1),
                       "bright": int(cent[s:e].mean()), "mid": round(float(vocal_ratio[s:e].mean()),2)})
    out["blocks"]=blocks
    # find quietest 10s window after 40% of song (bridge) and loudest 10s (climax)
    w=10
    sm = np.convolve(rms_db[:n], np.ones(w)/w, mode='valid')
    start = int(n*0.4)
    out["climax_at"] = int(np.argmax(sm))
    out["quietest_after_40pct_at"] = start+int(np.argmin(sm[start:n-w])) if n-w>start else None
    out["intro_loud_first15"] = round(float(rms_db[:15].mean()),1)
    out["dynamic_range_db"] = round(float(sm.max()-sm[start:].min()),1)
    return out

for p in sys.argv[1:]:
    r = analyze(p)
    print("=== ", p.split('/')[-1])
    print(json.dumps({k:v for k,v in r.items() if k!="blocks"}))
    for b in r["blocks"]:
        print(f'{b["t"]:>5}  loud {b["loud"]:6.1f}  drums {b["drums"]:6.1f}  bright {b["bright"]:5d}  mid {b["mid"]:.2f}')
