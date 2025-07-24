% -*- coding: utf-8 -*-
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{sty/eiiatfg}[2015/07/03 modified book class for UCLM EII TFG]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\PassOptionsToClass{11pt,twoside,titlepage,openright,a4paper}{book}
\ProcessOptions\relax
\LoadClass{book}

\setlength{\unitlength}{1mm}

% https://tug.org/pipermail/pstricks/2011/009122.html
\usepackage{etex}

% Codificación UTF8
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[spanish,es-tabla,es-noshorthands]{babel}
\usepackage[backend=biber,
    labelnumber,
    style=ieee,
    citestyle=numeric-comp,
    sorting=none]{biblatex}
%\usepackage[
%    backend=biber, 
    %style=ieee,
    %style=alphabetic,
%    style=ieee-alphabetic,
%    sorting=nty]{biblatex}
\usepackage[hyperfootnotes=false]{hyperref}
\usepackage{times}
\usepackage{enumerate}
\usepackage{enumitem}
\usepackage{bookmark}
\usepackage{datetime2}
\usepackage{makecell}
\usepackage[dvipsnames]{xcolor}
\usepackage{multirow}
\usepackage[%
    font={small,sf},
    labelfont=bf,
    format=hang,    
    format=plain,
    margin=0pt,
    width=0.8\textwidth,
]{caption}
\usepackage[list=true]{subcaption}
\usepackage{appendix}
\usepackage{listings}
\usepackage{longtable}
\usepackage{tabularx}
\usepackage{colortbl}
\usepackage{minted}
\usepackage[export]{adjustbox}
\usepackage{emptypage}
\usepackage{setspace}
\usepackage{textcomp}
\usepackage{footmisc}
\usepackage{csquotes}
\usepackage{rotating}
\usepackage{wrapfig}
\usepackage{xstring}
\usepackage{pdfpages}
\usepackage{amsmath}
\usepackage{cleveref}
\usepackage{ifthen}
\usepackage{currfile}

\usepackage[
  paperwidth=210mm,
  paperheight=297mm,
  left=35mm,right=30mm,
  top=25mm, bottom=25mm,
  marginparwidth=1cm, marginparsep=1cm]{geometry}

\captionsetup{
  margin=0pt,
  font={footnotesize,stretch=.85},
  labelfont=bf}

\setlength{\parskip}{4pt}

\makeatletter
\providecommand*{\input@path}{}
\g@addto@macro\input@path{{tex/}{sty/}}
\makeatother
\graphicspath{{fig/}}

\pagestyle{headings}

\renewcommand{\bibname}{Referencias}
\renewcommand{\appendixname}{Anexo}
\renewcommand{\appendixtocname}{Anexo}
\renewcommand{\appendixpagename}{Anexo}

\definecolor{gris30}{gray}{0.30}
\definecolor{gris85}{gray}{0.85}
\definecolor{gris20}{gray}{0.20}
\definecolor{gris50}{gray}{0.50}
\newcommand\myshade{85}
\colorlet{mylinkcolor}{violet}
\colorlet{mycitecolor}{YellowOrange}
\colorlet{myurlcolor}{Aquamarine}

\hypersetup{
  linkcolor  = mylinkcolor!\myshade!black,
  citecolor  = mycitecolor!\myshade!black,
  urlcolor   = myurlcolor!\myshade!black,
  colorlinks = true,
}

\usepackage{metadata}
\usepackage{licencia}
\usepackage{code}
\usepackage{portada}
\usepackage{entornos}
\usepackage{indices}
\usepackage{admonition}


\setlist[description]{style=nextline,labelwidth=0pt,leftmargin=30pt,itemindent=\dimexpr-20pt-\labelsep\relax} % Global Setup Description List

\DeclareRobustCommand{\deschyperlink}[2]{%
  \hyperlink{#1}{#2}%
}


\if0 % Conflicto con acrónimos
\makeatletter % Redefinition of Description List Items source: http://tex.stackexchange.com/a/1248/13552
\let\orgdescriptionlabel\descriptionlabel
\renewcommand*{\descriptionlabel}[1]{%
  \let\orglabel\label
  \let\label\@gobble
  \phantomsection
  \protected@edef\@currentlabel{#1}%
  %\edef\@currentlabelname{#1}%
  \let\label\orglabel
  \orgdescriptionlabel{#1}%
}
\makeatother
\fi