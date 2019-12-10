MINING_TIME  = 10      # Tiempo q se supone q se mine un bloque
MINING_ROUND = 5        # se mina mining_round bloques en mining_time segundos
MINING_LIMIT = 20       # cantidad máxima de mensajes q puede estar contenida en un bloque
SPACE        = 2 ** 256 # espacio de llaves sobre el cual se aplica la dificultad

from message import Message
BLOCK_CONTAINER = Message

GENESIS_BLOCK = "{\"index\": 0, \"nonce\": 0, \"timestamp\": 0, \"previous\": \"NONE\", \"difficulty\": 1000, \"content\": [\"{\\\"data\\\": \\\"Hello World From Blockchain\\\", \\\"hash\\\": \\\"1b4c878aea01ffd70803426843f28d0c8f83342175528685bd7cf4a671a8466e\\\"}\"], \"merkle\": \"5af7a60f7b6bc1a291096f1b85513a3a3faef6f4bd54175ab107978243f0388a\", \"hash\": \"cbc750e95e066eb3aa56f3392c3dbd34b8988e53ee8b899b1e3b6f48393cb638\"}" 