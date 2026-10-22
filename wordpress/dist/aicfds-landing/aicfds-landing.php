<?php
/**
 * Plugin Name:       AIC × Fondazione di Sardegna – Landing page progetto
 * Description:       Aggiunge il modello di pagina «Progetto Fondazione di Sardegna»: landing page one page del progetto interregionale, con header e footer del tema.
 * Version:           1.0.0
 * Requires at least: 6.3
 * Requires PHP:      7.4
 * Text Domain:       aicfds-landing
 *
 * Come si usa: Pagine → Aggiungi nuova → Attributi pagina → Modello → «Progetto Fondazione di Sardegna».
 * Il contenuto della pagina (editor) non viene usato: le sezioni sono in template-parts/.
 */

defined( 'ABSPATH' ) || exit;

define( 'AICFDS_VERSION', '1.0.0' );
define( 'AICFDS_PATH', plugin_dir_path( __FILE__ ) );
define( 'AICFDS_URL', plugin_dir_url( __FILE__ ) );
define( 'AICFDS_TEMPLATE', 'aicfds-progetto-fondazione.php' );

/**
 * URL di un file in assets/ (loghi, immagini, CSS, JS).
 *
 * @param string $path Percorso relativo a assets/, es. 'logos/aic-sardegna.png'.
 * @return string
 */
function aicfds_asset( $path ) {
	return AICFDS_URL . 'assets/' . ltrim( $path, '/' );
}

/**
 * Vero se la pagina corrente usa il nostro modello.
 *
 * @return bool
 */
function aicfds_is_landing() {
	return is_singular( 'page' ) && get_page_template_slug() === AICFDS_TEMPLATE;
}

/** Registra il modello nell'elenco «Modello» degli attributi pagina. */
add_filter(
	'theme_page_templates',
	function ( $templates ) {
		$templates[ AICFDS_TEMPLATE ] = __( 'Progetto Fondazione di Sardegna', 'aicfds-landing' );
		return $templates;
	}
);

/**
 * Carica il template del plugin al posto di quello del tema.
 * Priorità alta: deve vincere anche sul Theme Builder di Elementor Pro.
 */
add_filter(
	'template_include',
	function ( $template ) {
		return aicfds_is_landing() ? AICFDS_PATH . 'templates/page-progetto-fondazione.php' : $template;
	},
	99
);

/** Classe sul body, utile per eventuali regole CSS di pagina. */
add_filter(
	'body_class',
	function ( $classes ) {
		if ( aicfds_is_landing() ) {
			$classes[] = 'aicfds-landing';
		}
		return $classes;
	}
);

/** CSS e JS solo sulle pagine che usano il modello. La versione segue la data del file (cache busting). */
add_action(
	'wp_enqueue_scripts',
	function () {
		if ( ! aicfds_is_landing() ) {
			return;
		}

		$css = AICFDS_PATH . 'assets/css/aicfds.css';
		wp_enqueue_style( 'aicfds-landing', aicfds_asset( 'css/aicfds.css' ), array(), (string) filemtime( $css ) );

		$js = AICFDS_PATH . 'assets/js/aicfds.js';
		wp_enqueue_script(
			'aicfds-landing',
			aicfds_asset( 'js/aicfds.js' ),
			array(),
			(string) filemtime( $js ),
			array(
				'in_footer' => true,
				'strategy'  => 'defer',
			)
		);
	},
	20
);
