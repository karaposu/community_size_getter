/etc/systemd/system


Reload systemd so it sees your new files:
sudo systemctl daemon-reload


Enable the timer to start at boot:
sudo systemctl enable save_sizes_job.timer


Start the timer now (so it’s active)
sudo systemctl start save_sizes_job.timer




Check the timer status
systemctl status save_sizes_job.timer



Trigger a manual run:
sudo systemctl start save_sizes_job.service


You can then check logs via
journalctl -u save_sizes_job.service