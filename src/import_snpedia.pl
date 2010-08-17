#!/usr/bin/env perl
use MediaWiki::Bot;
my $bot = MediaWiki::Bot->new();
$bot->set_wiki('www.snpedia.com','/');

foreach my $rs ('rs1815739',
                'rs4420638',
                'rs6152') {
   my $text = $bot->get_text($rs);
   print '=' x 20,"$rs\n";
   print $text;
}