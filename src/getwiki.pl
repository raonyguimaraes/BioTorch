#!/usr/bin/env perl
use MediaWiki::Bot;
my $bot = MediaWiki::Bot->new();
$bot->set_wiki('www.snpedia.com','/');
my @rsnums = $bot->get_pages_in_category('Category:Is_a_snp');
print "@rsnums";
