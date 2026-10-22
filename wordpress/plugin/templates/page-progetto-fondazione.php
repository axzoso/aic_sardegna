<?php
/**
 * Template Name: Progetto Fondazione di Sardegna
 * Template Post Type: page
 *
 * Header e footer sono quelli del sito (Theme Builder di Elementor Pro, richiamati dal tema).
 * Il contenuto è composto dalle sezioni in ../template-parts/, incluse in ordine alfabetico (01-, 02-, …).
 *
 * @package aicfds-landing
 */

defined( 'ABSPATH' ) || exit;

get_header();
?>

<main id="content" class="aicfds">
<?php
$aicfds_parts = glob( AICFDS_PATH . 'template-parts/*.php' );
sort( $aicfds_parts );
foreach ( $aicfds_parts as $aicfds_part ) {
	include $aicfds_part;
}
?>
</main>

<?php
get_footer();
