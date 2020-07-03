# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"日记本", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.tc_title = wx.TextCtrl( self, wx.ID_ANY, u"请输入笔记标题", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.tc_title, 0, wx.ALL|wx.EXPAND, 5 )

		self.tc_detail = wx.TextCtrl( self, wx.ID_ANY, u"请输入笔记详情", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.tc_detail, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.btn_save = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.btn_save, 0, wx.ALL, 5 )

		self.btn_clear = wx.Button( self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.btn_clear, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer2, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.btn_save.Bind( wx.EVT_BUTTON, self.save_content )
		self.btn_clear.Bind( wx.EVT_BUTTON, self.clear_content )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def save_content( self, event ):
		event.Skip()

	def clear_content( self, event ):
		event.Skip()


