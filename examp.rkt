;;; #lang racket
;;; (define (sum x y)
;;;     (+ x y))

;;; (define (subtract x y)
;;;     (- x y))

;;; (define (multiply x y)
;;;     (* x y))

;;; (define (divide x y)
;;;     (/ x y))

;;; (define (odd? x)
;;;     (= (modulo x 2) 1))

;;; (define (even? x)
;;;     (= (modulo x 2) 0))


(define (greater? x y)
    (>= x y))

(define (less? x y)
    (<= x y))

(define (equal? x y)
    (= x y))

(define (not-equal? x y)
    (not (= x y)))

(define (and? x y)
    (and x y))

(define (or? x y)
    (or x y))

(define (not? x)
    (not x))


; test
(greater?  5 10)
(less? 10 5)
(equal? 10 5)
(not-equal? 10 5)
(and? #t #f)
(or? #t #f)
(not? #t)

(print "Hello, World!")


(define a 10)
(define b 5)
