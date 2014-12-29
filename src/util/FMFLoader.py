#!/usr/bin/env python
# -*- coding: Shift-JIS -*-

'''
I used "FMF Loader" made by Mr.Kenmo.
See http://d.hatena.ne.jp/kenmo/20060509#p1
So Mr.Kenmo has rights of this souce code, be careful.
'''

import struct

class Layer2D:
	""" 2次元レイヤー """
	def __init__(self, width, height):
		"""
		コンストラクタ
		@param width  幅
		@param height 高さ
		"""
		self.width  = width
		self.height = height
		self.size   = width*height  # データサイズ
		self.data   = ()
	def get(self, i, j):
		if 0 <= i < self.width:
			if 0 <= j < self.height:
				return self.data[j*self.width + i]
		return None
	def __str__(self):
		strData = "  "
		for i, data in enumerate(self.data):
			strData += "%r,"%data
			if (i+1) % self.width == 0:
				strData += "\n  "
		return "(Width,Height)=(%d,%d)\n%s"%(
			self.width, self.height, strData)

class FMFLoader:
	""" FMFファイル読込クラス """
	# データのbit数に対応するバイトコード変換関数テーブル
	READ_FUNC_TBL = {
		8:  lambda b: struct.unpack("B", b)[0],
		16: lambda b: struct.unpack("H", b)[0],
	}
	def __init__(self, filepath, layer2d=Layer2D):
		"""
		コンストラクタ
		@param filepath FMFファイルパス
		@param layer    レイヤーとして使用するクラス(Layer2Dの派生クラス）
		"""
		self.filepath = filepath
		self.file     = open(filepath, "rb")
		# ヘッダ
		self._readHeader()
		# データ（ レイヤーリスト）
		self.layerList = map(self._createLayer, [layer2d]*self.layerCount)
	def _readHeader(self):
		""" ヘッダ読込[20byte] """
		b = self.file.read(4)
		self.identifier = b  # ファイル識別子       [4byte]
		b = self.file.read(16)
		(self.dataSize,      # ヘッダを除いたサイズ [4byte]
			self.width,      # マップの幅           [4byte]
			self.height,     # マップの高さ         [4byte]
			self.chipWidth,  # チップの幅           [1byte]
			self.chipHeight, # チップの高さ         [1byte]
			self.layerCount, # レイヤー数           [1byte]
			self.bitCount    # データのbit数(8/16)  [1byte]
		) = struct.unpack("LLLBBBB", b)
	def _createLayer(self, layer2d):
		""" レイヤーの生成 """
		return self._setLayerData(
			apply(layer2d, (self.width, self.height)),
			0,
			self._readData())
	def _setLayerData(self, layer, idx, var):
		"""
		レイヤーにデータを設定
		@param layer レイヤーオブジェクト
		@param idx   インデックス
		@param var   値
		"""
		if idx < layer.size:
			layer.data += var,
			return self._setLayerData(layer, idx+1, self._readData())
		else:
			self.file.seek(-self.bitCount/8, 1) # １つ戻す
			return layer
	def _readData(self):
		"""
		データ読込
		@return 読込データ（EOFの場合None）
		"""
		return self._convertData(
			self.file.read(self.bitCount/8),
			self.READ_FUNC_TBL[self.bitCount])
	def _convertData(self, b, convert):
		"""
		データの変換
		@param b       バイナリコード
		@param convert 変換関数
		@return 変換後のデータ（終わりの場合None）
		"""
		if b == "": return None # 終わり
		else      : return convert(b)
	def getLayer(self, idx):
		"""
		レイヤーオブジェクト取得
		@parma idx レイヤー番号
		"""
		if 0 <= idx < self.layerCount:
			return self.layerList[idx]
		return None
	def strHeader(self):
		return "%s%s%s%s%s%s%s%s"%(
		"  Identifier         :%s\n"%self.identifier,
		"  Size(except Header):%i\n"%self.dataSize,
		"  Width              :%i\n"%self.width,
		"  Height             :%i\n"%self.height,
		"  ChipWidth          :%i\n"%self.chipWidth,
		"  ChipHeight         :%i\n"%self.chipHeight,
		"  LayerCount         :%i\n"%self.layerCount,
		"  BitCount           :%i\n"%self.bitCount,
		)
	def strData(self):
		result = "  "
		for idx, layer in enumerate(self.layerList):
			result += "[Layer:%d]\n  "%idx
			for i, data in enumerate(layer.data):
				result += "%r,"%data
				if (i+1) % layer.width == 0:
					result += "\n  "
		return result
	def __str__(self):
		header = self.strHeader()
		data   = self.strData()
		return "Header ... \n%s\nData ... \n%s"%(header, data)
def main():
	fmf = FMFLoader("area.fmf")
	print fmf

if __name__ == "__main__":
	main()
