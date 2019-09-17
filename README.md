# Wescap (Wesnoth Capture Tool)

Wescap is a Python app which helps to dump and decode the communication traffic between the Battle for Wesnoth client and the game server.

## Requirements

- Python 3
- Wireshark

## Usage

Use `-h` flag for more info.

### Dumping tool

```
python dump.py -t wireshark_dir/tshark -i eth0 -p 15000 14999 -e -o dump.csv
```

### Dump parser

```
python decode.py dump.csv -e
```

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)
