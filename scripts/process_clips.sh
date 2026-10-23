set -e
cd "$(dirname "$0")/../clips_raw"
ENC="-c:v libx264 -crf 10 -preset slow -pix_fmt yuv420p -r 24 -an"
WM="delogo=x=1852:y=1032:w=56:h=36"
MI="minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1"
# plain: watermark + no audio
for n in 4 5 6 7 8 9 14 18 20 21 23 28 29 30 31 32 32a; do
  ffmpeg -v error -y -i "$n.mp4" -vf "$WM" $ENC "../clips_clean/$n.mp4"; echo "ok $n"
done
# 2: upscale then watermark
ffmpeg -v error -y -i 2.mp4 -vf "scale=1920:1080:flags=lanczos,$WM" $ENC ../clips_clean/2.mp4; echo ok 2
# 11: patch bezel from left of mark, no audio
ffmpeg -v error -y -i "11 소리 빼기.mp4" -filter_complex "[0:v]split[a][b];[b]crop=60:40:1790:1030[p];[a][p]overlay=1850:1030" $ENC ../clips_clean/11.mp4; echo ok 11
# 12: 2x speed -> 4s
ffmpeg -v error -y -i "12 2배속 하기.mp4" -vf "$WM,setpts=0.5*PTS" $ENC ../clips_clean/12.mp4; echo ok 12
# 13: 1.5x -> ~2.5s
ffmpeg -v error -y -i "13 1.5배속 하기.mp4" -vf "$WM,setpts=PTS/1.5" $ENC ../clips_clean/13.mp4; echo ok 13
# 15: 2.54s -> 5s
ffmpeg -v error -y -i "15 필요한 만큼 초 늘리기.mp4" -vf "$WM,setpts=1.97*PTS,$MI" $ENC ../clips_clean/15.mp4; echo ok 15
# 22: 1.6s -> 4s
ffmpeg -v error -y -i "22 원하는 만큼 초 늘리기.mp4" -vf "$WM,setpts=2.5*PTS,$MI" $ENC ../clips_clean/22.mp4; echo ok 22
# 19 candidate
ffmpeg -v error -y -i "19 후보, 엔진 모양이 달라서 고민.mp4" -vf "$WM" $ENC "../clips_clean/19 후보.mp4"; echo ok 19
# 25: already clean
cp 25.mp4 ../clips_clean/25.mp4; echo ok 25
echo ALLDONE
