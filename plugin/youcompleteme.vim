" Copyright (C) 2011  Strahinja Markovic  <strahinja.markovic@gmail.com>
"
" This file is part of YouCompleteMe.
"
" YouCompleteMe is free software: you can redistribute it and/or modify
" it under the terms of the GNU General Public License as published by
" the Free Software Foundation, either version 3 of the License, or
" (at your option) any later version.
"
" YouCompleteMe is distributed in the hope that it will be useful,
" but WITHOUT ANY WARRANTY; without even the implied warranty of
" MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
" GNU General Public License for more details.
"
" You should have received a copy of the GNU General Public License
" along with YouCompleteMe.  If not, see <http://www.gnu.org/licenses/>.

if exists("g:loaded_youcompleteme")
  finish
endif
let g:loaded_youcompleteme = 1

" This is basic vim plugin boilerplate
let s:save_cpo = &cpo
set cpo&vim

" On-demand loading. Let's use the autoload folder and not slow down vim's
" startup procedure.
augroup youcompletemeStart
  autocmd!
  autocmd VimEnter * call youcompleteme#Enable()
augroup END

" This is basic vim plugin boilerplate
let &cpo = s:save_cpo
unlet s:save_cpo