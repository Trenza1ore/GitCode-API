:orphan:

418 I'm a teapot
================

.. rubric:: Request rejected with maximum tea energy

This endpoint refuses to brew coffee.

Per `RFC 2324 <https://datatracker.ietf.org/doc/html/rfc2324>`__, the server
is proudly operating in **teapot mode** and therefore declines all
coffee-related duties.

.. code-block:: http

   HTTP/1.1 418 I'm a teapot
   Content-Type: text/plain; charset=utf-8
   X-Teapot-Status: steeping
   X-Coffee-Request: denied

   Short and stout.
   Tip me over and pour me out.

.. topic:: Diagnostic summary
   :class: gc-doc-card

   **Status:** ``418 I'm a teapot``

   **Cause:** Someone tried to make coffee with tea infrastructure.

   **Suggested fix:** Try tea, hot water, or lowering your expectations.

.. note::

   If you were actually looking for the API docs, back away slowly from the
   kettle and return to :doc:`the documentation homepage <index>`.

.. rubric:: Troubleshooting

1. Confirm the beverage is tea-adjacent.
2. Remove any espresso ambitions from the request payload.
3. Accept that the teapot has boundaries.
4. Order a cup of `heytea <https://www.heytea.com>`__ or something.
