from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

RPC_NODE = {
    "user": "OIDSAHdiasdiosudhasdjoasidjoaiqweoirof",
    "password": "sldkfhsooiAHOIDoIHJSOAKlsdjAOSIDao",
    "server": "127.0.0.1",
    "port": 8332
}


class ChainData:

    RPC_USER = RPC_NODE["user"]
    RPC_PASSWORD = RPC_NODE["password"]
    RPC_SERVER = RPC_NODE["server"]
    RPC_PORT = RPC_NODE["port"]

    def __init__(self, start_block, end_block):
        self.addresses = {}
        self.start_block = start_block
        self.end_block = end_block
        self.rpc_conn = AuthServiceProxy("http://%s:%s@%s:%s" % (
            self.RPC_USER, self.RPC_PASSWORD, self.RPC_SERVER, self.RPC_PORT))

    def get_blocks(self):
        resp = self.rpc_conn.getblockchaininfo()
        return resp["blocks"]

    def get_headers(self):
        resp = self.rpc_conn.getblockchaininfo()
        return resp["headers"]

    def get_blockhash(self, block):
        resp = self.rpc_conn.getblockhash(block)
        return resp

    def _get_blocktransactions(self, block):
        blockhash = self.get_blockhash(block)
        resp = self.rpc_conn.getblock(blockhash, 2)
        return resp["tx"], blockhash

    def getblock_out_addresses(self, block):
        txs, blockhash = self._get_blocktransactions(block)
        for tx in txs:
            for iout in tx['vout']:
                if iout.get("scriptPubKey") and iout.get("scriptPubKey").get("addresses"):
                    addresses = iout["scriptPubKey"]["addresses"]
                    for ad in addresses:
                        self.addresses[ad] = 1
                        print("block {}, address {}".format(block, ad))


if __name__ == "__main__":
    import sys
    print("Usage: ")
    print("parser.py <start-block> <end-block> parser-output.txt")
    start_block = int(sys.argv[1])
    end_block = int(sys.argv[2])
    output = sys.argv[3]
    cdata = ChainData(start_block=start_block, end_block=end_block)
    for i in range(start_block, end_block + 1):
        cdata.getblock_out_addresses(i)
    with open(output, "a+") as fl:
        for key in cdata.addresses.keys():
            fl.write("{}\r\n".format(key))
