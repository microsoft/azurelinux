sudo /home/damcilva/repos/temp/CBL-Mariner_TEMP2/toolkit/out/tools/bldtracker \
    --script-name=create_worker_chroot.sh \
    --log-file=/home/damcilva/repos/temp/CBL-Mariner_TEMP2/build/logs/worker_chroot.log \
    --out-path=/home/damcilva/repos/temp/CBL-Mariner_TEMP2/build/timestamp/chroot.json \
    --expected-steps=4 \
    --mode=init

sudo /home/damcilva/repos/temp/CBL-Mariner_TEMP2/toolkit/out/tools/bldtracker \
    --script-name=create_worker_chroot.sh \
    --log-file=/home/damcilva/repos/temp/CBL-Mariner_TEMP2/build/logs/worker_chroot.log \
    --out-path=/home/damcilva/repos/temp/CBL-Mariner_TEMP2/build/timestamp/chroot.json \
    '--step-path=start adding RPMs to worker chroot' \
    --expected-steps=0 \
    --mode=record

sudo /home/damcilva/repos/temp/CBL-Mariner_TEMP2/toolkit/out/tools/bldtracker \
    --script-name=create_worker_chroot.sh \
    --log-file=/home/damcilva/repos/temp/CBL-Mariner_TEMP2/build/logs/worker_chroot.log \
    --out-path=/home/damcilva/repos/temp/CBL-Mariner_TEMP2/build/timestamp/chroot.json \
    --mode=watch