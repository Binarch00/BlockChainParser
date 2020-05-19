from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import db
from settings import RPC_NODE
from multitask import IndexedTask, IndexedTaskManager


class ChainData:

    RPC_USER = RPC_NODE["user"]
    RPC_PASSWORD = RPC_NODE["password"]
    RPC_SERVER = RPC_NODE["server"]
    RPC_PORT = RPC_NODE["port"]

    def __init__(self):
        self.db1 = db.DataBase()
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
        count = 0
        for tx in txs:
            for iout in tx['vout']:
                if iout.get("scriptPubKey") and iout.get("scriptPubKey").get("addresses"):
                    addresses = iout["scriptPubKey"]["addresses"]
                    for ad in addresses:
                        count += 1
                        self.db1.add_unique(ad)


class BlockParserIndexedTask(IndexedTask):

    speed_step = 10  # speed in seconds to process 10 blocks
    speed_in_minutes = True

    def distributed_task(self, index):
        print("Processing block {}".format(index))
        cdata = ChainData()
        cdata.getblock_out_addresses(index)


if __name__ == "__main__":
    import sys
    print("Usage: ")
    print("parser.py <start-block> <end-block> <num of parse process>")
    print("Use same input to allow resume/continue paused or interrupted blocks")

    start_block = int(sys.argv[1])
    end_block = int(sys.argv[2])
    process_num = int(sys.argv[3])

    itm = IndexedTaskManager(start_block, end_block, BlockParserIndexedTask, split=process_num)
    itm.run()
