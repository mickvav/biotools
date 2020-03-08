#!/bin/bash
sudo mkdir /mnt/data
mkdir /home/ubuntu/reference_contig_fasta
cat >> /etc/fstab << EOF
ip-172-31-24-63:/mnt/data /mnt/data nfs  ro 0 0
ip-172-31-24-63:/home/ubuntu/reference_contig_fasta /home/ubuntu/reference_contig_fasta nfs  rw,sync 0 0
EOF
sudo apt -y install nfs-common
sudo mount -a
