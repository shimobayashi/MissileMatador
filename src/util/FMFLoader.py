#!/usr/bin/env python
# -*- coding: Shift-JIS -*-

'''
I used "FMF Loader" made by Mr.Kenmo.
See http://d.hatena.ne.jp/kenmo/20060509#p1
So Mr.Kenmo has rights of this souce code, be careful.
'''

import struct

class Layer2D:
	""" 2�������C���[ """
	def __init__(self, width, height):
		"""
		�R���X�g���N�^
		@param width  ��
		@param height ����
		"""
		self.width  = width
		self.height = height
		self.size   = width*height  # �f�[�^�T�C�Y
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
	""" FMF�t�@�C���Ǎ��N���X """
	# �f�[�^��bit���ɑΉ�����o�C�g�R�[�h�ϊ��֐��e�[�u��
	READ_FUNC_TBL = {
		8:  lambda b: struct.unpack("B", b)[0],
		16: lambda b: struct.unpack("H", b)[0],
	}
	def __init__(self, filepath, layer2d=Layer2D):
		"""
		�R���X�g���N�^
		@param filepath FMF�t�@�C���p�X
		@param layer    ���C���[�Ƃ��Ďg�p����N���X(Layer2D�̔h���N���X�j
		"""
		self.filepath = filepath
		self.file     = open(filepath, "rb")
		# �w�b�_
		self._readHeader()
		# �f�[�^�i ���C���[���X�g�j
		self.layerList = map(self._createLayer, [layer2d]*self.layerCount)
	def _readHeader(self):
		""" �w�b�_�Ǎ�[20byte] """
		b = self.file.read(4)
		self.identifier = b  # �t�@�C�����ʎq       [4byte]
		b = self.file.read(16)
		(self.dataSize,      # �w�b�_���������T�C�Y [4byte]
			self.width,      # �}�b�v�̕�           [4byte]
			self.height,     # �}�b�v�̍���         [4byte]
			self.chipWidth,  # �`�b�v�̕�           [1byte]
			self.chipHeight, # �`�b�v�̍���         [1byte]
			self.layerCount, # ���C���[��           [1byte]
			self.bitCount    # �f�[�^��bit��(8/16)  [1byte]
		) = struct.unpack("LLLBBBB", b)
	def _createLayer(self, layer2d):
		""" ���C���[�̐��� """
		return self._setLayerData(
			apply(layer2d, (self.width, self.height)),
			0,
			self._readData())
	def _setLayerData(self, layer, idx, var):
		"""
		���C���[�Ƀf�[�^��ݒ�
		@param layer ���C���[�I�u�W�F�N�g
		@param idx   �C���f�b�N�X
		@param var   �l
		"""
		if idx < layer.size:
			layer.data += var,
			return self._setLayerData(layer, idx+1, self._readData())
		else:
			self.file.seek(-self.bitCount/8, 1) # �P�߂�
			return layer
	def _readData(self):
		"""
		�f�[�^�Ǎ�
		@return �Ǎ��f�[�^�iEOF�̏ꍇNone�j
		"""
		return self._convertData(
			self.file.read(self.bitCount/8),
			self.READ_FUNC_TBL[self.bitCount])
	def _convertData(self, b, convert):
		"""
		�f�[�^�̕ϊ�
		@param b       �o�C�i���R�[�h
		@param convert �ϊ��֐�
		@return �ϊ���̃f�[�^�i�I���̏ꍇNone�j
		"""
		if b == "": return None # �I���
		else      : return convert(b)
	def getLayer(self, idx):
		"""
		���C���[�I�u�W�F�N�g�擾
		@parma idx ���C���[�ԍ�
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
