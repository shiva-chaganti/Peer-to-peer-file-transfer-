﻿# Peer-to-peer-file-transfer-
﻿
﻿MODEL  : Pure P2P
OS USED : Windows 8
IDEA :  
•	Peer initially sends a request to its neighbor peers and fetches the list of peers it's connected to. The list of peers in displayed on GUI. 
•	If a new peer is added or removed in the network, a notification pop will be displayed indicating whether the peer has been added or removed.
•	Then once the peer is connected, it checks whether all its peers are alive periodically. The connection is checked continuously to maintain the connection while file transfer.
•	Peer fetches the list of available files from other connected peers. 
•	The user selects the file he/she wants to download. A popup is displayed to choose the location for saving the chosen file after download.
•	Peer then start downloading the selected file from the list and save on the desired location. A progress bar is also displayed which shows the download status.
•	Also, calculates the download time for each file.

	PREREQUISITES
•	Connect at least two peers on the same network.
•	Reliable network must be available.

	EXECUTION STEPS
•	Extract the P2P.zip file. The contents of the package will be displayed.
I.	Interface.py
II.	Peer_str.py
III.	Comm.py

•	Execute Interface.py.

o	python /path_to_file/Interface.py

•	The GUI has options 
I.	Download
II.	File Info
III.	Refresh
When clicked on any file from file list and clicked on Download, we can see a progress bar showing the download status.
When clicked on File Info, the file list of the peer is displayed. If any new files have been added, on click on File Info again, the new files added are displayed.
When clicked on Refresh, the peer list is updated and notification popup regarding a peer addition or peer removal will be displayed.
•	Select any connected peer from the peer list and click on File Info button to fetch the file list.
•	Select the file to be downloaded from the list and click on Download button. A progress bar will be seen which shows the download status.
•	The time taken to download will be shown on the terminal.

